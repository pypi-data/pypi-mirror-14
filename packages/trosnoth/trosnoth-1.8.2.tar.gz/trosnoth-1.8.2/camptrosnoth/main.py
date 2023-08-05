# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2011 Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import getpass
import os

from twisted.internet import defer

from trosnoth.run.main import Main
import trosnoth.main
from trosnoth.trosnothgui.pregame.authServerLoginBox import PasswordGUI
from trosnoth.trosnothgui.pregame.playscreen import PlayAuthScreen
from trosnoth.trosnothgui.pregame.serverSelectionScreen import (
        ServerSelectionScreen)
from trosnoth.trosnothgui.pregame.startup import StartupInterface
from trosnoth.trosnothgui.interface import SingleAuthInterface, Interface

class CampPasswordGetter(object):
    def getPassword(self, host, errorText=''):
        create = False
        username = getpass.getuser()
        password = username.encode('rot13')
        return defer.succeed((create, username, password))

class CampPlayAuthScreen(PlayAuthScreen):
    @staticmethod
    def passwordGUIFactory(app):
        if os.environ.get('LTSP_CLIENT'):
            return CampPasswordGetter()
        return PasswordGUI(app)


class CampSingleAuthInterface(SingleAuthInterface):
    connectScreenFactory = CampPlayAuthScreen

class CampServerSelectionScreen(ServerSelectionScreen):
    connectScreenFactory = CampPlayAuthScreen

class CampStartupInterface(StartupInterface):
    connectScreenFactory = CampPlayAuthScreen
    serverScreenFactory = CampServerSelectionScreen

class CampInterface(Interface):
    def _makeStartupInterface(self):
        return CampStartupInterface(self.app, self)

class CampMain(Main):
    singleInterfaceFactory = CampSingleAuthInterface
    standardInterfaceFactory = CampInterface

class main(trosnoth.main.main):
    appFactory = CampMain

if __name__ == '__main__':
    main()
