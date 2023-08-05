import os
from setuptools import find_packages, setup

# Select appropriate modules
modules = find_packages('python')
scripts = ['bin/catidb_ui']
pkgdata = {
    'catidb_ui': ['*.ui'],
}
release_info = {}
execfile(os.path.join(os.path.dirname('__file__'), 'python', 'catidb_api', 'info.py'), release_info)

# Build the setup
setup(
    name=release_info["NAME"],
    description=release_info["DESCRIPTION"],
    license=release_info["LICENSE"],
    author=release_info["AUTHOR"],
    author_email=release_info["AUTHOR_EMAIL"],
    version=release_info["VERSION"],
    url=release_info["URL"],
    # All modules are in the python directory
    package_dir = {'': 'python'},
    packages=modules,
    package_data=pkgdata,
    install_requires=release_info["REQUIRES"],
    scripts=scripts
)
