#from distutils.core import setup

__version__ = '0.1.0'


METADATA = dict(
    name = 'python-crawler',
    version = __version__,
    py_modules = ['pycrawlerlib'],
    description = 'Python  web crawler',
    long_description = '',
    license='Apache License 2.0',
    author = 'Yifei Jiang',
    author_email = 'jiangyifei@gmail.com',
    url = 'http://code.google.com/p/pycrawlerlib/',
    keywords='web crawler python module',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6.x",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        ],
)

SETUPTOOLS_METADATA = dict(
  install_requires=['lxml', 'bsddb3',],
  include_package_data = True,

)

try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)
