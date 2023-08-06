from collections import namedtuple
from morepath.autosetup import (
    caller_module, caller_package, autosetup,
    morepath_packages, import_package)
from base.m import App
import morepath
import pytest


def setup_module(module):
    morepath.disable_implicit()


def test_import():
    import base
    import sub
    import entrypoint
    from ns import real
    from ns import real2
    import under_score

    assert sorted(list(morepath_packages()),
                  key=lambda module: module.__name__) == [
                      base, entrypoint, real, real2, sub, under_score]


def test_load_distribution():

    Distribution = namedtuple('Distribution', ['project_name'])

    assert import_package(Distribution('base')).m.App is App

    with pytest.raises(morepath.error.AutoImportError):
        import_package(Distribution('inexistant-package'))


def invoke(callable):
    "Add one frame to stack, no other purpose."
    return callable()


def test_caller_module():
    import sys
    assert caller_module(1) == sys.modules[__name__]
    assert invoke(caller_module) == sys.modules[__name__]


def test_caller_package():
    import sys
    assert caller_package(1) == sys.modules[__package__]
    assert invoke(caller_package) == sys.modules[__package__]


def test_autosetup(monkeypatch):
    import sys

    for k in 'base.m', 'entrypoint.app', 'under_score.m':
        monkeypatch.delitem(sys.modules, k, raising=False)

    pytest.deprecated_call(autosetup)

    assert 'base.m' in sys.modules
    assert 'entrypoint.app' in sys.modules
    assert 'under_score.m' in sys.modules
