import io
import re
import os

from setuptools import find_namespace_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
# with io.open("README.md", "rt", encoding="utf8") as f:
#     readme = f.read()


install_requires = []
with io.open("requirements.txt", "rt", encoding="utf8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue

        install_requires.append(line)

extras_require = {}
packages = ['ie']
packages.extend(find_namespace_packages(include=['ie.*']))

setup(
    name='app',
    version='1.0',
    packages=packages,
    include_package_data=True,
    long_description=__doc__,
    python_requires=">=3.6,<3.10",
    setup_requires=["setuptools>=40.0"],
    zip_safe=False,
    install_requires=['Flask']
)