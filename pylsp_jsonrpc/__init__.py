# Copyright 2017-2020 Palantir Technologies, Inc.
# Copyright 2021- Python Language Server Contributors.

from . import _version
from ._version import __version__


def convert_version_info(version: str) -> (int, ..., str):
    version_info = version.split(".")
    for i in range(len(version_info)):  # pylint:disable=consider-using-enumerate
        try:
            version_info[i] = int(version_info[i])
        except ValueError:
            version_info[i] = version_info[i].split("+")[0]
            version_info = version_info[: i + 1]
            break

    return tuple(version_info)


_version.VERSION_INFO = convert_version_info(__version__)

__all__ = ("__version__",)
