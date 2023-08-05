# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

_package_data = dict(
    full_package_name="virtualenvutils",
    version_info=(0, 2, 3),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="manage virtualenv based utilities",
    keywords="virtualenv utilities",
    entry_points='virtualenvutils=virtualenvutils.__main__:main',
    # entry_points=None,
    license="MIT License",
    since=2016,
    # status: "α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    install_requires=dict(
        any=["ruamel.appconfig", "ruamel.std.argparse", "ruamel.std.pathlib"],
        # py27=["ruamel.ordereddict"],
    ),
)


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val

version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version
