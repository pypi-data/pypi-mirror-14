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

from twisted.internet import defer

from trosnoth.run.authserver import (AuthenticationFactory, AuthManager,
        AuthenticatedUser)
import trosnoth.run.authserver

class CampAuthManager(AuthManager):
    def authenticateUser(self, username, password):
        username = username.lower()
        if password == username.encode('rot13'):
            user = AuthenticatedUser(self, username)
            user.seen()
            return defer.succeed(user)
        return super(CampAuthManager, self).authenticateUser(username, password)

class CampAuthenticationFactory(AuthenticationFactory):
    authManagerClass = CampAuthManager

class main(trosnoth.run.authserver.main):
    authFactory = CampAuthenticationFactory

if __name__ == '__main__':
    main()

