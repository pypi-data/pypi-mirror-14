"""
    trackdeps.tracker
    Track dependencies versions and which one needs updates

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import datetime

import requests
from packaging import specifiers, version

from . import parser


PYPI_URL = "https://pypi.python.org/pypi"


class UnknowDependency(Exception):
    """A dependency wasn't found on PyPI"""


class Dependency:
    """Representation of a dependency"""

    def __init__(self, package):
        self.package = package
        self.needed_by = {}
        self.requires_updates = {}

        self._needed_by_raw = []

        self.latest_update = -1
        self.latest_release = None

        self.get_status()

    def add_requirement(self, requirement):
        """Add a thing which requires this dependency"""
        file = requirement["file"]
        project = requirement["project"]

        specifier = None
        if requirement["specifier"] is not None:
            specifier = specifiers.Specifier(requirement["specifier"])

        if project not in self.needed_by:
            self.needed_by[project] = {}

        self.needed_by[project][file] = specifier
        self._needed_by_raw.append(requirement)

        if specifier is None:
            return

        # Update the self.requires_updates
        if self.latest_release not in specifier:
            if project not in self.requires_updates:
                self.requires_updates[project] = []
            self.requires_updates[project].append(file)

    def get_status(self):
        """Get the dependency status from PyPI"""
        response = requests.get(PYPI_URL+"/"+self.package+"/json")
        if response.status_code >= 400:
            raise UnknowDependency("Can't find "+self.package+" on PyPI")
        content = response.json()

        # Calculate the latest release
        # The one provided by PyPI is not used to avoid tracking pre-releases,
        # but if errors are found while parsing the versions, that will be used
        # as a fallback
        try:
            releases = [version.Version(r) for r in content["releases"].keys()]
            latest = None
            for release in releases:
                # Skip pre-releases
                if release.is_prerelease:
                    continue

                if latest is None or release > latest:
                    latest = release
        except version.InvalidVersion:
            latest = content["info"]["version"]

        self.latest_release = str(latest)
        uploaded = content["releases"][self.latest_release][0]["upload_time"]
        converted = datetime.datetime.strptime(uploaded, "%Y-%m-%dT%H:%M:%S")
        self.latest_update = converted.timestamp()


def track_requirements_file(path, base="/", project=None):
    """Track a requirements.txt file"""
    parsed = parser.parse_requirements(path, base, project)
    return _track_parsed(parsed)


def track_setup_file(path, base="/", project=None):
    """Track dependencies in a setup.py file"""
    parsed = parser.parse_setup(path, base, project)
    return _track_parsed(parsed)


def _track_parsed(parsed):
    """Actually do the tracking"""
    deps = {}

    for requirement in parsed:
        if requirement["package"] not in deps:
            deps[requirement["package"]] = Dependency(requirement["package"])

        deps[requirement["package"]].add_requirement(requirement)

    return deps


def merge_results(*results):
    """Merge multiple results you got"""
    packages = {}
    result = {}

    # First of all merge togheter all the results
    for result in results:
        for name, package in result.items():
            if name not in packages:
                packages[name] = []
            packages[name].append(package)

    # And then merge the Dependency objects
    for name, deps in packages.items():
        result[name] = merge_dependency(*deps)

    return result


def merge_dependency(*deps):
    """Merge together multiple Dependency objects"""
    package = None
    dependency = None

    # Some optimizations
    if not len(deps):
        return None
    elif len(deps) == 1:
        return deps[0]

    for dep in deps:
        # Initialize the Dependency the first iteration
        if package is None:
            package = dep.package
            dependency = Dependency(package)

        # Merge only the same dependency
        if dep.package != package:
            raise ValueError("Can't merge Dependency of different packages!")

        for requirement in dep._needed_by_raw:
            dependency.add_requirement(requirement)

    return dependency
