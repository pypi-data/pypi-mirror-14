# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2012 Joshua D Bartlett
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

import logging

from trosnoth.messages import AwardPlayerStarMsg, RemoveCollectableStarMsg
from trosnoth.model.unit import Bouncy, CollectableUnit

log = logging.getLogger('star')


class CollectableStar(Bouncy, CollectableUnit):
    # The following values control star movement.
    maxFallVel = 540            # pix/s
    gravity = 1000              # pix/s/s
    initVel = 480

    HALF_WIDTH = 5
    HALF_HEIGHT = 5

    def __init__(self, world, id, pos, *args, **kwargs):
        super(CollectableStar, self).__init__(world, *args, **kwargs)
        self.id = id
        self.creationTime = self.world.timer.getElapsedTime()
        self.vanished = False

        # Place myself.
        self.pos = pos
        self.xVel = 0
        self.yVel = 0

    def collidedWithPlayer(self, player):
        self.world.sendServerCommand(AwardPlayerStarMsg(player.id))

        if self.vanished:
            # It's already been removed from the main set of stars.
            self.world.deadStars.remove(self)
        else:
            del self.world.collectableStars[self.id]
            self.world.sendServerCommand(RemoveCollectableStarMsg(self.id))

    def removeDueToTime(self):
        self.vanished = True
        self.world.deadStars.add(self)
        del self.world.collectableStars[self.id]
        self.world.sendServerCommand(RemoveCollectableStarMsg(self.id))

    def getGravity(self):
        return self.gravity

    def getMaxFallVel(self):
        return self.maxFallVel
