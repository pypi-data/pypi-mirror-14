#!/usr/bin/python
# -*- coding: utf-8 -*-

# daemon.py is a part of sun.

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

"""
 ____  _   _ _   _
/ ___|| | | | \ | |
\___ \| | | |  \| |
 ___) | |_| | |\  |
|____/ \___/|_| \_|

"""

import time
import urllib2
import pynotify
import commands
from utils import (
    config,
    fetch,
    mirror
)
from __metadata__ import (
    __all__,
    icon_path
)


class Notify(object):
    """Main notify Class
    """
    def __init__(self):
        pynotify.uninit()
        pynotify.init("sun")
        self.pkg_count = fetch()[0]
        self.message_added = ""
        self.summary = "{0}Software Updates".format(" " * 14)
        self.message = ("{0}{1} Software updates are available\n".format(
            " " * 3, self.pkg_count))
        self.icon = "{0}{1}.png".format(icon_path, __all__)
        self.n = pynotify.Notification(self.summary, self.message, self.icon)
        self.n.set_timeout(60000 * int(config()["STANDBY"]))

    def gtk_loaded(self):
        """Check if gtk icon running
        """
        out = commands.getoutput("ps -A")
        if "sun_gtk" in out:
            return True

    def show(self):
        """Startup dbus message if packages
        """
        if self.pkg_count > 0 and self.gtk_loaded():
            self.n.show()     # show notification


def main():

    while True:
        connection = True
        time.sleep(1)
        try:
            urllib2.urlopen(mirror())
        except urllib2.URLError:
            connection = False
        except ValueError:
            pass
        if connection:
            Notify().show()
            time.sleep(60 * int(config()["INTERVAL"]))

if __name__ == "__main__":
    main()
