from setuptools import setup, find_packages
from os import path
import re

# Get current path
here = path.abspath(path.dirname(__file__))

# Get version from _.version.py
with open(path.join(here, 'packagecloudpoll/_version.py')) as f:
    version_file = f.read()
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                          version_file, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

# Get long description from README and HISTORY
with open(path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(path.join(here, 'HISTORY.rst')) as f:
    history = f.read()

# Dependencies
requires = [
    'docopt',
    'requests',
    'schema',
]

setup(
    name='packagecloud-poll',
    version=version,
    description='Polls the packagecloud.io API until a package filename is found.',
    long_description=readme + '\n\n' + history,
    author='Paul Liu',
    author_email='paul@ferociouspings.com',
    url='https://github.com/pwyliu/packagecloud-poll',
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
    ],
    keywords='packagecloud.io packagecloud packagecloud-poll packaging CI',
    install_requires=requires,
    include_package_data=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['packagecloud-poll = packagecloudpoll.poll:main']
    },
)
