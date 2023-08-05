"""
    trackdeps.report
    Report generator for trackdeps

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import os.path
import subprocess
import tempfile
import shutil
import glob
import base64
import time
import sys

import yaml
import jinja2
import csscompressor
import htmlmin.minify

from . import tracker


class GenerationError(Exception):
    pass


def format_day(timestamp):
    """Format a timestamp"""
    return time.strftime("%d/%m/%Y", time.gmtime(timestamp))


def track_deps(config):
    """Track dependecies from a config file"""
    with open(config) as f:
        config = yaml.load(f.read())

    tracked = []

    for project, subconfig in config.items():
        try:
            directory = tempfile.mkdtemp()

            # Clone the repository locally
            subprocess.call(["git", "clone", subconfig["git-url"], directory,
                             "--depth=1"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

            if subconfig["setup"] is not None:
                path = os.path.join(directory, subconfig["setup"])
                tracked.append(tracker.track_setup_file(path, directory,
                                                        project))

            if subconfig["requirements"] is not None:
                for requirement in subconfig["requirements"]:
                    path = os.path.join(directory, requirement)

                    # Support wildcards in the path name
                    if "*" not in path and "?" not in path:
                        paths = [path]
                    else:
                        paths = glob.glob(path)
                    for one in paths:
                        res = tracker.track_requirements_file(one, directory,
                                                              project)
                        tracked.append(res)

        finally:
            shutil.rmtree(directory)

    return tracker.merge_results(*tracked)


def render_report(deps):
    """Render a report with a specific output"""
    base = os.path.join(os.path.dirname(__file__), "html")

    # Calculate which dependencies needs to be updated
    requires_updates = []
    for dep in deps.values():
        if not len(dep.requires_updates):
            continue
        requires_updates.append(dep)
    requires_updates.sort(key=lambda i: i.package)

    # Get the minified stylesheet
    with open(os.path.join(base, "style.css")) as f:
        minified_stylesheet = csscompressor.compress(f.read())

    # Get the base64-encoded favicon
    favicon = "green.ico"
    if len(requires_updates):
        favicon = "orange.ico"
    with open(os.path.join(base, favicon), "rb") as f:
        base64_favicon = base64.b64encode(f.read()).decode("ascii")

    # Render the rendering environment
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(base))
    env.filters["format_day"] = format_day

    tmpl = env.get_template("template.html")
    res = tmpl.render(requires_updates=requires_updates,
                      minified_stylesheet=minified_stylesheet,
                      base64_favicon=base64_favicon)

    return htmlmin.minify.html_minify(res)


def generate(config, output, force=False):
    """Generate a new report"""
    config = os.path.expanduser(config)
    output = os.path.expanduser(output)

    # Config file il required
    if not os.path.exists(config):
        raise GenerationError("Configuration file %s not found" % config)

    # Don't override existing files, thx
    if output != "-" and os.path.exists(output) and not force:
        raise GenerationError("The output file %s already exists!" % output)

    tracked = track_deps(config)
    rendered = render_report(tracked)

    # - is the standard output
    if output == "-":
        sys.stdout.write(rendered)
    else:
        with open(output, "w") as f:
            f.write(rendered)
