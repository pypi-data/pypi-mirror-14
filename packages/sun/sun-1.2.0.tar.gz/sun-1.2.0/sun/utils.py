#!/usr/bin/python
# -*- coding: utf-8 -*-

# utils.py is a part of sun.

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
import re
import getpass
import urllib2
from __metadata__ import (
    pkg_path,
    conf_path,
    etc_slackpkg,
    changelog_txt,
    var_lib_slackpkg
)


def urlopen(link):
    """Return urllib2 urlopen
    """
    try:
        return urllib2.urlopen(link)
    except urllib2.URLError:
        pass
    except ValueError:
        return ""
    except KeyboardInterrupt:
        print("")
        raise SystemExit()


def read_file(registry):
    """Return reading file
    """
    with open(registry, "r") as file_txt:
        read_file = file_txt.read()
        file_txt.close()
        return read_file


def slack_ver():
    """Open file and read Slackware version
    """
    dist = read_file("/etc/slackware-version")
    sv = re.findall(r"\d+", dist)
    if len(sv) > 2:
        version = (".".join(sv[:2]))
    else:
        version = (".".join(sv))
    return dist.split()[0], version


def ins_packages():
    """Count installed Slackware packages
    """
    count = 0
    for pkg in os.listdir(pkg_path):
        if not pkg.startswith("."):
            count += 1
    return count


def read_config(config):
    """Read config file and return uncomment line
    """
    for line in config.splitlines():
        line = line.lstrip()
        if line and not line.startswith("#"):
            return line
    return ""


def mirror():
    """Get mirror from slackpkg mirrors file
    """
    slack_mirror = read_config(
        read_file("{0}{1}".format(etc_slackpkg, "mirrors")))
    if slack_mirror:
        return slack_mirror + changelog_txt
    else:
        print("\nYou do not have any mirror selected in /etc/slackpkg/mirrors"
              "\nPlease edit that file and uncomment ONE mirror.\n")
        return ""


def fetch():
    """Get ChangeLog.txt file size and count upgraded packages
    """
    mir, r, slackpkg_last_date = mirror(), "", ""
    count, upgraded = 0, []
    if mir:
        tar = urlopen(mir)
        try:
            r = tar.read()
        except AttributeError:
            print("sun: error: can't read mirror")
    count = 0
    if os.path.isfile(var_lib_slackpkg + changelog_txt):
        slackpkg_last_date = read_file("{0}{1}".format(
            var_lib_slackpkg, changelog_txt)).split("\n", 1)[0].strip()
    else:
        return [count, upgraded]
    for line in r.splitlines():
        if slackpkg_last_date == line.strip():
            break
        if (line.endswith("Upgraded.") or line.endswith("Rebuilt.") or
                line.endswith("Added.")):
            upgraded.append(line.split("/")[-1])
            count += 1
    return [count, upgraded]


def config():
    """Return sun configuration values
    """
    conf_args = {
        "INTERVAL": 60,
        "STANDBY": 3
    }
    config_file = read_file("{0}{1}".format(conf_path, "sun.conf"))
    for line in config_file.splitlines():
        line = line.lstrip()
        if line and not line.startswith("#"):
            conf_args[line.split("=")[0]] = line.split("=")[1]
    return conf_args


def os_info():
    """Get OS info
    """
    stype = ""
    slack, ver = slack_ver()
    mir = mirror()
    if mir:
        if "current" in mir:
            stype = "Current"
        else:
            stype = "Stable"
    info = (
        "User: {0}\n"
        "OS: {1}\n"
        "Version: {2}\n"
        "Type: {3}\n"
        "Arch: {4}\n"
        "Kernel: {5}\n"
        "Packages: {6}".format(getpass.getuser(), slack, ver, stype,
                               os.uname()[4], os.uname()[2], ins_packages()))
    return info
