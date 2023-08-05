#!/usr/bin/python
# -*- coding: utf-8 -*-

# setup.py file is part of sun.

# Copyright 2015-2016 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://github.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import shutil

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sun.__metadata__ import (
    __all__, __version__,
    __email__, __author__,
    conf_path, icon_path,
    desktop_path
)

INSTALLATION_REQUIREMENTS = []
DOCS_REQUIREMENTS = []
TESTS_REQUIREMENTS = []
OPTIONAL_REQUIREMENTS = []


setup(
    name=__all__,
    packages=["sun", "sun/gtk", "sun/cli"],
    scripts=["bin/sun_daemon", "bin/sun", "bin/sun_gtk"],
    version=__version__,
    description="Tray notification applet for informing about package updates "
                "in Slackware",
    keywords=["tray", "notify", "slackware", "desktop"],
    author=__author__,
    author_email=__email__,
    url="https://github.com/dslackw/sun",
    package_data={"": ["LICENSE", "README.rst", "ChangeLog.txt"]},
    install_requires=INSTALLATION_REQUIREMENTS,
    extras_require={
        "optional": OPTIONAL_REQUIREMENTS,
        "docs": DOCS_REQUIREMENTS,
        "tests": TESTS_REQUIREMENTS,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later "
        "(GPLv3+)",
        "Classifier: Operating System :: POSIX :: Linux",
        "Classifier: Programming Language :: Python :: 2.7",
        "Classifier: Topic :: Desktop Environment",
        "Classifier: Topic :: System :: Monitoring"
        ],
    long_description=open("README.rst").read()
)

# Install configs, .desktop and icon via pip
if "install" in sys.argv:
    dirs = [conf_path, icon_path, desktop_path]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
    print("Install sun.conf --> {0}".format(conf_path))
    shutil.copy2("conf/{0}.conf".format(__all__), conf_path)
    print("Install sun.png --> {0}".format(icon_path))
    shutil.copy2("icon/{0}.png".format(__all__), icon_path)
    print("Install sun.desktop --> {0}".format(desktop_path))
    shutil.copy2("{0}.desktop".format(__all__), desktop_path)
