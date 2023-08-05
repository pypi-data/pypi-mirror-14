import pytest

from defrost import Package, Requirement


@pytest.mark.parametrize("freeze, expected", [
    ("", False),
    ("foobar==1.2.3", True),
    ("foo==1.2.3\nbar==2.0", True),
])
def test_pip_freeze__bool(freeze, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert bool(pip_freeze) is expected


@pytest.mark.parametrize("freeze, expected", [
    ("", []),
    ("foobar==1.2.3", [Package("foobar==1.2.3")]),
    ("foo==1.2.3\nbar==2.0", [Package("foo==1.2.3"), Package("bar==2.0")]),
    ("-f /opt/pip/wheels\n-e git+git@github.com:SurveyMonkey/defrost.git\nfoo==1.2.3\n## !! Could not determine repository location\nbar==2.0", [Package("foo==1.2.3"), Package("bar==2.0")]),
    ("## FIXME: could not find svn URL in dependency_links for this package:\ndeveloperweb===3-update-etcdev-r0", [Package("developerweb===3-update-etcdev-r0")]),
    ("-i https://pypi.python.org/simple\nfoo==1.2.3", [Package("foo==1.2.3")]),  # test -i
    ("foo==1.2.3\n\nbar==2.0\n\n", [Package("foo==1.2.3"), Package("bar==2.0")]),  # test blank lines
    (b"foo==1.2.3\nbar==2.0", [Package("foo==1.2.3"), Package("bar==2.0")]),  # test pip freeze as bytes
])
def test_pip_freeze__iter(freeze, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert list(pip_freeze) == expected


@pytest.mark.parametrize("freeze, expected", [
    ("", 0),
    ("foobar==1.2.3", 1),
    ("foo==1.2.3\nbar==2.0", 2),
])
def test_pip_freeze__len(freeze, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert len(pip_freeze) == expected


@pytest.mark.parametrize("freeze, package, expected", [
    ('foo==1.2', 'foo', True),
    ('foo==1.2', 'FOO', True),
    ('foo==1.2', 'foo==1.2', True),
    ('foo==1.2', 'foo>=1.0', True),
    ('foo==1.2', 'foo<2.0', True),
    ("foobar==1.2", 'foobar>=1.0,<2.0', True),
    ('foo==1.2', Requirement('foo'), True),
    ('foo==1.2', Requirement('foo==1.2'), True),
    ('foo==1.2', Requirement('foo>=1.0'), True),
    ('foo==1.2', Package('foo==1.2'), True),
    ('foo==1.2\nbar==1.0', 'bar', True),
    ("foo==1.2\nbar==2.0", 'foobar', False),
    ('foo==1.2', 'bar', False),
    ('foo==1.2', 'foo==1.3', False),
    ('foo==1.2', Requirement('bar'), False),
    ('foo==1.2', Requirement('foo==1.3'), False),
    ('foo==1.2', Requirement('foo>=2.0'), False),
    ('foo==1.2', Requirement('bar==1.2'), False),
    ('foo==1.2', Package('bar==1.2'), False),
    ("", "foo==1.2", False),
])
def test_pip_freeze__contains(freeze, package, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert (package in pip_freeze) is expected


@pytest.mark.parametrize("freeze, package, expected", [
    ('foo==1.2', 'foo', Package('foo==1.2')),
    ('foo==1.2', 'FOO', Package('foo==1.2')),
    ('foo==1.2\nbar==1.0', 'bar', Package('bar==1.0')),
])
def test_pip_freeze__getitems_found(freeze, package, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert pip_freeze[package] == expected


@pytest.mark.parametrize("freeze, package", [
    ('foo==1.2', 'bar'),
])
def test_pip_freeze__getitems_KeyError(freeze, package):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    pytest.raises(KeyError, pip_freeze.__getitem__, package)


@pytest.mark.parametrize("freeze, package, expected", [
    ('foo==1.2', 'bar', None),
    ('foo==1.2', 'foo', Package('foo==1.2')),
    ('foo==1.2', 'FOO', Package('foo==1.2')),
])
def test_pip_freeze__get_without_default(freeze, package, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert pip_freeze.get(package) == expected


@pytest.mark.parametrize("freeze, package, default, expected", [
    ('foo==1.2', 'bar', None, None),
    ('foo==1.2', 'bar', 'some-default', 'some-default'),
    ('foo==1.2', 'foo', 'some-default', Package('foo==1.2')),
    ('foo==1.2', 'FOO', 'some-default', Package('foo==1.2')),
])
def test_pip_freeze__get_with_default(freeze, package, default, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert pip_freeze.get(package, default) == expected


@pytest.mark.parametrize("freeze, reqs, expected_deprecated", [
    ("foo==1.2", {'requirements': [{'requirement': 'foo', 'reason': 'hello'}]}, []),
    ("foo==1.2", {'requirements': [{'requirement': 'foo<1.0', 'reason': 'upgrade'}]}, [('foo==1.2', 'upgrade', 'error')]),
    ("foo==1.2", {'requirements': [{'requirement': 'foo>=1.0', 'reason': 'upgrade'}]}, []),
    ("foo==1.2\nbar==2.0", {'requirements': [
        {'requirement': 'foo>=1.0', 'reason': 'upgrade'},
        {'requirement': 'bar<2.0', 'reason': 'downgrade'}]}, [('bar==2.0', 'downgrade', 'error')]),
    ("foo==1.2", {'requirements': []}, []),
    ("foo==1.2", {'requirements': [{'requirement': 'bar>=1.0', 'reason': 'upgrade'}]}, []),
    ("foo==1.2", {'requirements': [{'requirement': 'foo<1.0', 'reason': 'upgrade', 'severity': 'warn'}]}, [('foo==1.2', 'upgrade', 'warn')]),
    ("foo==1.2", {'requirements': [{'requirement': 'foo<1.0', 'severity': 'warn'}]}, [('foo==1.2', None, 'warn')]),
])
def test_pip_freeze__load_requirements(freeze, reqs, expected_deprecated):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    pip_freeze.load_requirements(reqs)
    assert len(pip_freeze.deprecated) == len(expected_deprecated)
    for package, (pin, reason, severity) in zip(pip_freeze.deprecated, expected_deprecated):
        assert package.deprecated is True
        assert str(package) == pin
        assert package.deprecation_reason == reason
        assert package.deprecation_severity == severity
