"""
    trackdeps.parser
    Parse requirements.txt and setup.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import glob
import re
import os
import subprocess
import shutil
import tempfile


_line_re = re.compile(r'^([a-zA-Z0-9\-_\.]+)((===?|>=?|<=?|~=).*)?$')


class InvalidLineError(Exception):
    pass


class FailedSetupCall(Exception):
    pass


def _get_filename(path, base):
    """Get a filename relative to ``base``"""
    path = os.path.abspath(path)
    base = os.path.abspath(base)

    # path must be a subdirectory of base
    if not path.startswith(base):
        return None

    # Normalize base
    if base[-1] != "/":
        base = base+"/"
    elif base == "/":
        base = ""

    return path[len(base):]


def _parse_line(line, filename="", project=None):
    """Return all the information contained in a specific line"""
    line = line.strip()  # Remove some whitespaces

    parsed = _line_re.match(line)
    if parsed is None:
        raise InvalidLineError("Line '%s' doesn't match" % line)

    result = parsed.groups()
    package = result[0]
    if len(result) > 1:
        specifier = result[1]

    return {"package": package, "project": project, "specifier": specifier,
            "file": filename}


def parse_requirements(path, base="/", project=None):
    """Parse a requirements file"""
    path = os.path.expanduser(path)
    base = os.path.expanduser(base)

    filename = _get_filename(path, base)
    if filename is None:
        raise ValueError("%s is not a subdirectory of %s" % (path, base))

    with open(path) as f:
        content = f.read()

    result = []
    for line in content.split("\n"):
        # Ignore empty lines
        if line.strip() == "":
            continue

        # CLI arguments are not supported
        if line[0] == "-":
            continue

        # Remove comments
        if "#" in line:
            line = line.split("#", 1)[0]

        try:
            result.append(_parse_line(line, filename, project))
        except InvalidLineError:
            pass

    return result


def parse_setup(path, base="/", project=None):
    """Parse a setup.py file"""
    path = os.path.expanduser(path)
    base = os.path.expanduser(base)

    filename = _get_filename(path, base)
    if filename is None:
        raise ValueError("%s is not a subdirectory of %s" % (path, base))

    tempdir = tempfile.mkdtemp()
    try:
        res = subprocess.call(["python3", path, "egg_info", "-e", tempdir],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL,
                              cwd=os.path.dirname(os.path.abspath(path)))

        # Return code != 0 means something went wrong
        if res != 0:
            raise FailedSetupCall("setup.py returned non-zero error code")

        # Since it's a new directory the only sub-directory should be the one
        # created by setuptools
        requirements = glob.glob(os.path.join(tempdir, "*", "requires.txt"))[0]
        with open(requirements) as f:
            content = f.read()

        result = []
        for line in content.split("\n"):
            # Ignore empty lines
            if line.strip() == "":
                continue

            result.append(_parse_line(line, filename, project))

        return result

    # Be sure to remove the temp directory
    finally:
        shutil.rmtree(tempdir)
