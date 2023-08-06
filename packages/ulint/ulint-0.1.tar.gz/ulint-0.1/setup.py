
import os
import errno

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


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


try:
    symlink(os.path.join(SOURCE_DIR, 'pre-commit'),
            os.path.join(SOURCE_DIR, '.git', 'hooks', 'pre-commit'))
except OSError as error:
    if error.errno != errno.EEXIST:
        raise

try:
    import pandoc
    doc = pandoc.Document()
    doc.markdown = open('README.md').read().encode()
    description = doc.rst.decode("utf-8")
except (IOError, ImportError) as e:
    description = ''


setup(
    name="ulint",
    version="0.1",
    author="Thibault Saunier",
    author_email="tsaunier@gnome.org",
    description=("Utility and library to easily run linters on your source"
                 " code handling virtually any language"),
    license="LGPL",
    keywords="lint tool code quality",
    url="http://packages.python.org/ulint",
    packages=['ulint'],
    long_description=description,
    classifiers=[
        "Topic :: Utilities",
         "License :: OSI Approved :: GNU Lesser General Public License v2 "
         "(LGPLv2) "
    ],
    install_requires=[
        'GitPython',
    ],
    scripts=['ulint/ulint'],
)
