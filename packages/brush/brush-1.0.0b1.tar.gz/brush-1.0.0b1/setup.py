import os.path
from setuptools import setup
from brush import __version__


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()

setup(
    name="brush",
    version=__version__,
    author="Michael V. DePalatis",
    author_email="depalatis@phys.au.dk",
    description="Monitor and log data from Menlo Systems optical frequency combs",
    long_description=read('README.rst'),
    license="MIT",
    keywords="physics science optical data acquisition",
    url="https://bitbucket.org/iontrapgroup/brush",
    install_requires=read('requirements.txt'),
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
