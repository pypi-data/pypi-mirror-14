import os
import errno

from distutils.core import Command
from setuptools import setup


SOURCE_DIR = os.path.abspath('./')


def symlink(source, link_name):
    """
    Method to allow creating symlinks on Windows
    """
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        os_symlink(source, link_name)
    else:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        if csl(link_name, source, flags) == 0:
            raise ctypes.WinError()


try:
    symlink(os.path.join(SOURCE_DIR, 'pre-commit'),
            os.path.join(SOURCE_DIR, '.git', 'hooks', 'pre-commit'))
except OSError as error:
    pass

try:
    import pandoc
    doc = pandoc.Document()
    doc.markdown = open('README.md').read().encode()
    description = doc.rst.decode("utf-8")
except (IOError, ImportError) as e:
    description = ''


setup(
    name="ulint-pep8",
    version="0.2",
    author="Thibault Saunier",
    author_email="tsaunier@gnome.org",
    description=("PEP8 linter for ulint"),
    license="LGPL",
    keywords="lint plugin pep8",
    url="http://packages.python.org/ulint-pep8",
    packages=['plugin'],
    classifiers=[
        "Topic :: Utilities",
         "License :: OSI Approved :: GNU Lesser General Public License v2 "
         "(LGPLv2) "
    ],
    install_requires=[
        'pep8', 'ulint',
    ],
    entry_points={
        'ulint.linters': 'pep8 = plugin.pep8linter:Linter'
    }
)
