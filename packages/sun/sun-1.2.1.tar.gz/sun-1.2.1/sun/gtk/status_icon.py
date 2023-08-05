#!/usr/bin/python
# -*- coding: utf-8 -*-

# sun_gtk is a part of sun.

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


import pygtk
pygtk.require("2.0")
import gtk
import subprocess
from sun.licenses import (
    lic, abt
)
from sun.__metadata__ import (
    __all__,
    __email__,
    __author__,
    __version__,
    __website__,
    bin_path,
    icon_path
)
from sun.cli.tool import (
    check_updates,
    daemon_status
)
from sun.utils import (
    os_info
)


class GtkStatusIcon(object):

    def __init__(self):
        self.dialog_title = ""
        self.daemon_STOCK = gtk.STOCK_YES
        self.sun_icon = "{0}{1}.png".format(icon_path, __all__)
        self.icon = gtk.status_icon_new_from_file(self.sun_icon)
        self.icon.connect("popup-menu", self.right_click)
        self.img = gtk.Image()
        self.img.set_from_file(self.sun_icon)
        self.icon.set_tooltip("Slackware Update Notifier")
        self.cmd = "{0}sun_daemon".format(bin_path)
        self.daemon_start()
        gtk.main()

    def daemon_start(self):
        """Start daemon when gtk loaded
        """
        if daemon_status() == "SUN not running":
            subprocess.call("{0} &".format(self.cmd), shell=True)

    def sub_menu(self):
        """Create daemon submenu
        """
        submenu = gtk.Menu()
        self.start = gtk.ImageMenuItem("Start")
        self.stop = gtk.ImageMenuItem("Stop")
        self.restart = gtk.ImageMenuItem("Restart")
        self.status = gtk.ImageMenuItem("Status")

        self.start.show()
        self.stop.show()
        self.restart.show()
        self.status.show()

        img_Start = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,
                                             gtk.ICON_SIZE_MENU)
        img_Start.show()
        self.start.set_image(img_Start)

        img_Stop = gtk.image_new_from_stock(gtk.STOCK_STOP,
                                            gtk.ICON_SIZE_MENU)
        img_Stop.show()
        self.stop.set_image(img_Stop)

        img_Restart = gtk.image_new_from_stock(gtk.STOCK_REFRESH,
                                               gtk.ICON_SIZE_MENU)
        img_Restart.show()
        self.restart.set_image(img_Restart)

        img_Status = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION,
                                              gtk.ICON_SIZE_MENU)
        img_Status.show()
        self.status.set_image(img_Status)

        submenu.append(self.start)
        submenu.append(self.stop)
        submenu.append(self.restart)
        submenu.append(self.status)

        self.daemon = gtk.ImageMenuItem("Daemon")
        self.img_daemon = gtk.image_new_from_stock(self.daemon_STOCK,
                                                   gtk.ICON_SIZE_MENU)
        self.img_daemon.show()
        self.daemon.set_submenu(submenu)

    def menu(self, event_button, event_time, data=None):
        """Create popup menu
        """
        self.sub_menu()
        menu = gtk.Menu()
        menu.append(self.daemon)

        separator = gtk.SeparatorMenuItem()

        menu_Check = gtk.ImageMenuItem("Check updates")
        img_Check = gtk.image_new_from_stock(gtk.STOCK_OK,
                                             gtk.ICON_SIZE_MENU)
        img_Check.show()

        menu_Info = gtk.ImageMenuItem("OS Info")
        img_Info = gtk.image_new_from_stock(gtk.STOCK_INFO,
                                            gtk.ICON_SIZE_MENU)
        img_Info.show()

        menu_About = gtk.ImageMenuItem("About")
        img_About = gtk.image_new_from_stock(gtk.STOCK_ABOUT,
                                             gtk.ICON_SIZE_MENU)
        img_About.show()

        self.daemon.set_image(self.img_daemon)
        menu.append(self.daemon)
        self.daemon.show()

        menu_Quit = gtk.ImageMenuItem("Quit")
        img_Quit = gtk.image_new_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_MENU)
        img_Quit.show()

        menu_Check.set_image(img_Check)
        menu_Info.set_image(img_Info)
        menu_About.set_image(img_About)
        menu_Quit.set_image(img_Quit)

        menu.append(menu_Check)
        menu.append(menu_Info)
        menu.append(separator)
        menu.append(menu_About)
        menu.append(menu_Quit)

        separator.show()
        menu_Check.show()
        menu_Info.show()
        menu_About.show()
        menu_Quit.show()

        menu_Check.connect_object("activate", self._Check, " ")
        menu_Info.connect_object("activate", self._Info, "OS Info")
        menu_About.connect_object("activate", self._About, "SUN")
        self.start.connect_object("activate", self._start, "Start daemon   ")
        self.stop.connect_object("activate", self._stop, "Stop daemon   ")
        self.restart.connect_object("activate", self._restart,
                                    "Restart daemon   ")
        self.status.connect_object("activate", self._status, daemon_status())
        menu_Quit.connect_object("activate", self._Quit, "stop")

        menu.popup(None, None, None, event_button, event_time, data)

    def message(self, data):
        """Function to display messages to the user
        """
        msg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                                gtk.BUTTONS_CLOSE, data)
        msg.set_resizable(1)
        msg.set_title(self.dialog_title)
        self.img.set_from_file(self.sun_icon)
        msg.set_image(self.img)
        msg.show_all()
        msg.run()
        msg.destroy()

    def right_click(self, data, event_button, event_time):
        """Right click handler
        """
        self.menu(event_button, event_time, data)

    def _Check(self, data):
        self.dialog_title = "SUN - Check updates"
        msg, count, packages = check_updates()
        data = msg
        if count > 0:
            if len(packages) > 10:
                packages = packages[:10] + ["and more..."]
            self.message("{0} \n{1}".format(data, "\n".join(packages)))
        else:
            self.message(data)

    def _Info(self, data):
        self.dialog_title = "SUN - " + data
        self.message(os_info())

    def _About(self, data):
        about = gtk.AboutDialog()
        about.set_destroy_with_parent(True)
        about.set_program_name(data)
        about.set_version(__version__)
        about.set_authors(["{0} <{1}>".format(__author__, __email__)])
        about.set_license("\n".join(lic))
        about.set_comments(abt)
        about.set_website(__website__)
        about.set_logo(gtk.gdk.pixbuf_new_from_file(self.sun_icon))
        about.run()
        about.destroy()

    def _start(self, data):
        self.dialog_title = "Daemon"
        subprocess.call("{0} &".format(self.cmd), shell=True)
        self.daemon_STOCK = gtk.STOCK_YES
        self.message(data)

    def _stop(self, data):
        self.dialog_title = "Daemon"
        subprocess.call("killall sun_daemon", shell=True)
        self.daemon_STOCK = gtk.STOCK_MEDIA_RECORD
        self.message(data)

    def _restart(self, data):
        self.dialog_title = "Daemon"
        subprocess.call("killall sun_daemon", shell=True)
        subprocess.call("{0} &".format(self.cmd), shell=True)
        self.daemon_STOCK = gtk.STOCK_YES
        self.message(data)

    def _status(self, data):
        self.dialog_title = "Daemon"
        self.message(data + " " * 3)

    def _Quit(self, data):
        del data
        gtk.main_quit()


def main():

    GtkStatusIcon()

if __name__ == "__main__":
    main()
