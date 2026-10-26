import importlib
import sys

import pytest

import respx._compat as compat


@pytest.fixture(autouse=True)
def restore_compat():
    yield
    importlib.reload(compat)


def test_invalid_package_env(monkeypatch):
    monkeypatch.setenv("RESPX_HTTPX_PACKAGE", "requests")
    with pytest.raises(ImportError, match="RESPX_HTTPX_PACKAGE"):
        importlib.reload(compat)


@pytest.mark.parametrize("package", ["httpx", "httpx2"])
def test_package_env(monkeypatch, package):
    monkeypatch.setenv("RESPX_HTTPX_PACKAGE", package)
    importlib.reload(compat)
    assert compat.httpx.__name__ == package


def test_fallback_to_httpx2(monkeypatch):
    monkeypatch.delenv("RESPX_HTTPX_PACKAGE", raising=False)
    monkeypatch.setitem(sys.modules, "httpx", None)
    importlib.reload(compat)
    assert compat.httpx_name == "httpx2"
    assert compat.httpcore_name == "httpcore2"


def test_none_installed(monkeypatch):
    monkeypatch.delenv("RESPX_HTTPX_PACKAGE", raising=False)
    monkeypatch.setitem(sys.modules, "httpx", None)
    monkeypatch.setitem(sys.modules, "httpx2", None)
    with pytest.raises(ImportError, match="httpx2"):
        importlib.reload(compat)
