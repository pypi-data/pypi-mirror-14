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
import os

from trosnoth.const import (
    OPEN_CHAT, GAME_FULL_REASON, UNAUTHORISED_REASON, NICK_USED_REASON,
    USER_IN_GAME_REASON, ALREADY_JOINED_REASON,
)
from trosnoth.model.agent import ConcreteAgent
from trosnoth.messages import (
    TaggingZoneMsg, ShootMsg, RespawnMsg, RespawnRequestMsg, TickMsg,
    CannotJoinMsg, UpdatePlayerStateMsg,
    AimPlayerAtMsg, BuyUpgradeMsg, ChatMsg,
)
from trosnoth.model.universe_base import NeutralTeamId
from trosnoth.utils.message import MessageConsumer
from trosnoth.utils.twist import WeakCallLater, WeakLoopingCall
import trosnoth.ais
from math import atan2

log = logging.getLogger('ai')


def listAIs(playableOnly=False):
    '''
    Returns a list of strings of the available AI classes.
    '''
    results = []
    try:
        files = os.listdir(os.path.dirname(trosnoth.ais.__file__))
    except OSError:
        # Probably frozen in a zip. Use a standard list.
        aiNames = ['alpha', 'simple', 'john', 'test']
    else:
        aiNames = [os.path.splitext(f)[0] for f in files if f.endswith('.py')]

    for aiName in aiNames:
        c = __import__('trosnoth.ais.%s' % (aiName,), fromlist=['AIClass'])
        if hasattr(c, 'AIClass') and (
                c.AIClass.playable or not playableOnly):
            results.append(aiName)
    return results


def makeAIAgent(game, aiName):
    c = __import__('trosnoth.ais.%s' % (aiName,), fromlist=['AIClass'])
    return AIAgent(game, c.AIClass)


class AIAgent(ConcreteAgent):
    '''
    Base class for an AI agent.
    '''

    def __init__(self, game, aiClass, *args, **kwargs):
        super(AIAgent, self).__init__(game=game, *args, **kwargs)
        self.aiClass = aiClass
        self.ai = None
        self.team = None
        self.requestedNick = None
        self._loop = WeakLoopingCall(self, '_tick')

    def start(self, team=None):
        self.team = team
        self._loop.start(2)

    def stop(self):
        super(AIAgent, self).stop()
        self._loop.stop()

    def _tick(self):
        if self.ai is not None:
            return
        if not self.world.state.aisEnabled():
            return

        nick = self.aiClass.nick

        if self.team is None:
            teamId = NeutralTeamId
        else:
            teamId = self.team.id

        self._joinGame(nick, teamId)

    def _joinGame(self, nick, teamId):
        self.requestedNick = nick
        nick = '%s-1' % (nick,)
        self.sendJoinRequest(teamId, nick, bot=True)

    @CannotJoinMsg.handler
    def _joinFailed(self, msg):
        r = msg.reasonId
        nick = self.requestedNick

        if r == GAME_FULL_REASON:
            message = 'full'
        elif r == UNAUTHORISED_REASON:
            message = 'not authenticated'
        elif r == NICK_USED_REASON:
            message = 'nick in use'
        elif r == USER_IN_GAME_REASON:
            message = 'user already in game'    # Should never happen
        elif r == ALREADY_JOINED_REASON:
            message = 'tried to join twice'     # Should never happen
        else:
            message = repr(r)

        log.error('Join failed for AI %r (%s)', nick, message)
        self.stop()

    def setPlayer(self, player):
        if player is None:
            log.debug('DISABLE AI: %s', self.ai)
            self.ai.disable()
            self.ai = None

        super(AIAgent, self).setPlayer(player)

        if player:
            self.requestedNick = None
            self.ai = self.aiClass(self.world, self.localState.player, self)

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        super(AIAgent, self).handle_TickMsg(msg)
        if self.ai:
            self.ai.consumeMsg(msg)

    def defaultHandler(self, msg):
        super(AIAgent, self).defaultHandler(msg)
        if self.ai:
            self.ai.consumeMsg(msg)


class AI(MessageConsumer):
    playable = False    # Change to True in playable subclasses.

    def __init__(self, world, player, agent, *args, **kwargs):
        super(AI, self).__init__(*args, **kwargs)
        self.world = world
        self.player = player
        self.player.onDied.addListener(self.died)
        self.agent = agent
        self.start()

    def sendRequest(self, msg):
        self.agent.sendRequest(msg)

    def start(self):
        raise NotImplementedError

    def disable(self):
        raise NotImplementedError

    def defaultHandler(self, msg):
        pass

    def _sendStateUpdate(self, key, value):
        self.sendRequest(UpdatePlayerStateMsg(
            value, stateKey=key, tickId=self.world.lastTickId))

    def doMoveRight(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('right', True)
        self._sendStateUpdate('left', False)

    def doMoveLeft(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('left', True)
        self._sendStateUpdate('right', False)

    def doStop(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('left', False)
        self._sendStateUpdate('right', False)

    def doDrop(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('down', True)
        WeakCallLater(0.1, self, '_releaseDropKey')

    def _releaseDropKey(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('down', False)

    def doJump(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('jump', True)

    def doStopJump(self):
        if self.alreadyRemoved():
            return
        self._sendStateUpdate('jump', False)

    def doAimAt(self, angle, thrust=1.0):
        if self.alreadyRemoved():
            return
        self.sendRequest(AimPlayerAtMsg(angle, thrust, self.world.lastTickId))

    def doAimAtPoint(self, pos, thrust=1.0):
        if self.alreadyRemoved():
            return
        x1, y1 = self.player.pos
        x2, y2 = pos
        angle = atan2(x2 - x1, -(y2 - y1))
        self.doAimAt(angle, thrust)

    def doShoot(self):
        if self.alreadyRemoved():
            return
        self.sendRequest(ShootMsg(self.world.lastTickId))

    def doRespawn(self):
        '''
        Attempts to respawn.
        '''
        if self.alreadyRemoved():
            return
        self.sendRequest(RespawnRequestMsg(self.world.lastTickId))

    def doBuyUpgrade(self, upgradeKind):
        '''
        Attempts to purchase an upgrade of the given kind.
        '''
        if self.alreadyRemoved():
            return
        self.sendRequest(BuyUpgradeMsg(
            upgradeKind.upgradeType, self.world.lastTickId))

    @RespawnMsg.handler
    def _respawned(self, msg):
        if msg.playerId == self.player.id:
            self.respawned()

    def respawned(self):
        pass

    def died(self, killer, deathType):
        pass

    @TaggingZoneMsg.handler
    def _zoneTagged(self, msg):
        self.zoneTagged(msg.zoneId, msg.playerId)

    def zoneTagged(self, zoneId, playerId):
        pass

    def doSendPublicChat(self, message):
        if self.alreadyRemoved():
            return
        self.sendRequest(ChatMsg(OPEN_CHAT, text=message.encode()))

    def alreadyRemoved(self):
        if self.player.id == -1:
            log.warning(
                'AI trying to continue after being removed: %s' %
                (self.__class__.__name__,))
            return True
        return False
