import io

from collections import OrderedDict
from .package import Package, Requirement


def _parse_pip_freeze(pip_freeze_output):
    if isinstance(pip_freeze_output, bytes):
        pip_freeze_output = pip_freeze_output.decode('utf-8')

    pip_freeze_output = io.StringIO(pip_freeze_output)

    for req in pip_freeze_output.readlines():
        req = req.strip()
        if not req or req.startswith(('-', '#')):
            continue
        yield Package(req)


def _to_requirement(requirement):
    if isinstance(requirement, Package):
        requirement = Requirement(str(requirement))

    elif isinstance(requirement, str):
        requirement = Requirement(requirement)

    return requirement


class PipFreeze(object):
    def __init__(self, pip_freeze_output):
        self._load_pip_freeze(pip_freeze_output)
        self.deprecated = []

    def _load_pip_freeze(self, pip_freeze_output):
        self._packages = OrderedDict()

        packages = _parse_pip_freeze(pip_freeze_output)
        for package in packages:
            self._packages[package.id] = package

    def __contains__(self, requirement):
        requirement = _to_requirement(requirement)
        package = self._packages.get(requirement.id)
        return package in requirement

    def __getitem__(self, package_name):
        requirement = _to_requirement(package_name)
        package = self._packages[requirement.id]
        return package

    def get(self, requirement, default=None):
        try:
            return self[requirement]
        except KeyError:
            return default

    def __iter__(self):
        for package in self._packages.values():
            yield package

    def __len__(self):
        return len(self._packages)

    def __nonzero__(self):
        # Python 2.x
        return self.__bool__()  # pragma: no cover

    def __bool__(self):
        # Python 3.x
        return bool(self._packages)

    def load_requirements(self, requirements):
        for req in requirements['requirements']:
            requirement = Requirement(req['requirement'])
            package = self._packages.get(requirement.id)
            if package is None:
                continue
            if package not in requirement:
                deprecate_kwargs = {'deprecated_by': requirement}
                if 'reason' in req:
                    deprecate_kwargs['reason'] = req['reason']
                if 'severity' in req:
                    deprecate_kwargs['severity'] = req['severity']
                package.deprecate(**deprecate_kwargs)
                self.deprecated.append(package)
