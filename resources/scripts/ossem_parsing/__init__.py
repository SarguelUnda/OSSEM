from .parser import load_ossem_dd, load_ossem_cdm, load_ossem_dm
from sys import version_info
assert version_info >= (3, 9), "Ossem parsing package need python 3.9 or later"

__all__ = [
    "load_ossem_dd",
    "load_ossem_cdm",
    "load_ossem_dm",
]
