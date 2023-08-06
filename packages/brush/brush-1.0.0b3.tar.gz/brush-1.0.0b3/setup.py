import os.path
from sys import version_info as pyver
from setuptools import setup
from brush import __version__


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()

requirements = [
    'six',
    'sqlalchemy',
    'pandas',
    'tornado'
]
if pyver.major == 2 or (pyver.major == 3 and pyver.minor <= 2):
    requirements.append('futures')

setup(
    name="brush",
    version=__version__,
    author="Michael V. DePalatis",
    author_email="depalatis@phys.au.dk",
    description="Monitor and log data from Menlo Systems optical frequency combs",
    long_description=read('README.rst'),
    license="MIT",
    keywords="physics science optics data acquisition frequency comb",
    url="https://bitbucket.org/iontrapgroup/brush",
    install_requires=requirements,
    packages=['brush'],
    package_data={
        'brush': [
            'static/css/*',
            'static/fonts/*',
            'static/img/*',
            'static/js/*',
            'templates/*'
        ]
    },
    entry_points={
        'console_scripts': ['brush=brush.cli:main']
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License'
    ]
)
