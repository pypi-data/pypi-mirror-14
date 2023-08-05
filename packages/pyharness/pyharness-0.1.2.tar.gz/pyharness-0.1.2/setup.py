from setuptools import setup, find_packages

from release import get_version

version = get_version('pyharness')
setup(
    name='pyharness',
    version=version,
    description='A lightweight framework for running experiments',
    author='Daniel Haas',
    author_email='thisisdhaas@gmail.com',
    url='https://github.com/thisisdhaas/pyharness',
    download_url=(
        'https://github.com/thisisdhaas/pyharness/tarball/v' + version),
    keywords=['experiments', 'harness'],
    classifiers=[],
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['pyharness=pyharness.command_line:main'],
    },
    include_package_data=True,
)
