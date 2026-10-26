"""
Select the HTTPX flavour (`httpx` or its fork `httpx2`) that RESPX mocks.

`httpx` is preferred when installed. `httpx2` (and its `httpcore2` dependency)
is used when `httpx` is missing, or when explicitly requested through the
`RESPX_HTTPX_PACKAGE=httpx2` environment variable.
"""

import importlib
import os
from types import ModuleType
from typing import Tuple

_PACKAGES = {"httpx": "httpcore", "httpx2": "httpcore2"}


def _select() -> Tuple[str, str]:
    requested = os.environ.get("RESPX_HTTPX_PACKAGE")
    if requested:
        if requested not in _PACKAGES:
            raise ImportError(
                f"RESPX_HTTPX_PACKAGE must be one of {sorted(_PACKAGES)}, "
                f"got {requested!r}"
            )
        return requested, _PACKAGES[requested]

    for name, core in _PACKAGES.items():
        try:
            importlib.import_module(name)
        except ImportError:
            continue
        return name, core

    raise ImportError("RESPX requires either `httpx` or `httpx2` to be installed")


httpx_name, httpcore_name = _select()
httpx: ModuleType = importlib.import_module(httpx_name)
httpcore: ModuleType = importlib.import_module(httpcore_name)
