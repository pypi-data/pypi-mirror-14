from distutils.core import setup, Extension

pyshoco = Extension('pyshoco', sources = ['pyshoco.c', 'shoco.c'], include_dirs = ['.'])

setup(name = 'pyshoco', version = '1.3.3', description = 'Shoco Python wrapper module', ext_modules = [pyshoco], author = 'R. Rowe', author_email = 'mega.gamer05@gmail.com', url = 'https://pypi.python.org/pypi/pyshoco/')