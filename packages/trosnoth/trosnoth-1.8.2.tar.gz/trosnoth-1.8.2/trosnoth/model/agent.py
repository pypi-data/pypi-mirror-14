import logging

from twisted.internet import reactor

from trosnoth.const import TICK_PERIOD, INITIAL_ASSUMED_LATENCY
from trosnoth.messages import (
    JoinRequestMsg, TickMsg, ResyncPlayerMsg, UpdatePlayerStateMsg,
    AimPlayerAtMsg, UpgradeApprovedMsg, PlayerHasUpgradeMsg, ShootMsg,
    CheckSyncMsg, WorldResetMsg, BuyUpgradeMsg, GameOverMsg,
)
from trosnoth.model.shot import LocalShot, LocalGrenade
from trosnoth.model.upgrades import Grenade
from trosnoth.utils.event import Event
from trosnoth.utils.message import MessageConsumer

log = logging.getLogger(__name__)

SYNC_CHECK_PERIOD = 3 / TICK_PERIOD


class Agent(object):
    '''
    Base class for things which can be connected to a Game using Game.addAgent.
    This may represent a user interface, an AI player, someone connecting over
    the network, or anything else that wants to receive interact with the game.
    '''

    def __init__(self, game, *args, **kwargs):
        super(Agent, self).__init__(*args, **kwargs)
        self.game = game
        self.player = None
        self.game.onServerCommand.addListener(self.gotServerCommand)

    def stop(self):
        '''
        Disconnects this agent from things that it's subscribed to and stops
        any active timed or looping calls.
        '''
        self.game.onServerCommand.removeListener(self.gotServerCommand)

    def gotServerCommand(self, msg):
        raise NotImplementedError(
            '%s.gotServerCommand' % (self.__class__.__name__,))

    def setPlayer(self, player):
        '''
        Called by the connected Game object when we are given authority to
        control the specified player. Also called with player=None when we no
        longer have the authority to control any player.
        '''
        self.player = player

    def messageToAgent(self, msg):
        '''
        Called by the connected Game object when there is a message
        specifically for this Agent (as opposed to a general game message).
        '''
        raise NotImplementedError(
            '%s.messageToAgent' % (self.__class__.__name__,))


class ConcreteAgent(Agent, MessageConsumer):
    '''
    Base class for Agents that actually represent the world (rather than
    proxying it through to the Network or some other agent).

    Note that a concrete agent is designed to represent only zero or one
    players.
    '''

    def __init__(self, *args, **kwargs):
        super(ConcreteAgent, self).__init__(*args, **kwargs)
        self.world = self.game.world
        self.localState = LocalState(self)
        self.lastPlayerAimSent = (None, None)
        self.nextSyncCheck = None

    def gotServerCommand(self, msg):
        msg.tracePoint(self, 'gotServerCommand')
        self.consumeMsg(msg)

    def messageToAgent(self, msg):
        msg.tracePoint(self, 'messageToAgent')
        self.consumeMsg(msg)

    def sendRequest(self, msg):
        msg.tracePoint(self, 'sendRequest')
        if not msg.clientValidate(
                self.localState, self.world, self._validationResponse):
            return
        msg.applyRequestToLocalState(self.localState)
        if isinstance(msg, AimPlayerAtMsg):
            # Special case: apply aim messages to the local state, but don't
            # indiscriminately send them to the server as they are mostly
            # cosmetic.
            return
        if isinstance(msg, ShootMsg) or (isinstance(msg, BuyUpgradeMsg)
                and msg.upgradeType == 'g'):
            # Special case: before shooting make sure the server knows what
            # direction we are facing.
            self.maybeSendAimMsg(self.world.lastTickId)
        reactor.callLater(0, self.game.agentRequest, self, msg)

    def _validationResponse(self, msg):
        self.consumeMsg(msg)

    def defaultHandler(self, msg):
        msg.tracePoint(self, 'defaultHandler')
        msg.applyOrderToLocalState(self.localState, self.world)

    def setPlayer(self, player):
        super(ConcreteAgent, self).setPlayer(player)
        if player:
            self.localState.playerJoined(player)
            self.resyncLocalPlayer({})
        else:
            self.localState.lostPlayer()

    @GameOverMsg.handler
    def handle_GameOverMsg(self, msg):
        if self.player is not None:
            self.localState.player.readyToStart = False
            self.localState.player.readyForTournament = False

    @WorldResetMsg.handler
    def handle_WorldResetMsg(self, msg):
        if self.player is not None:
            oldKeyState = dict(self.localState.player._state)
            self.localState.refreshPlayer()
            self.resyncLocalPlayer(oldKeyState)

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        self.maybeSendAimMsg(tickId=max(0, msg.tickId - 1))
        self.localState.tick()

        player = self.localState.player
        if player and self.nextSyncCheck <= msg.tickId:
            self.nextSyncCheck = msg.tickId + SYNC_CHECK_PERIOD
            self.sendRequest(CheckSyncMsg(
                self.world.lastTickId, player.pos[0],
                player.pos[1], player.yVel))

    def maybeSendAimMsg(self, tickId):
        '''
        Tell the server where the local player is facing.
        '''
        player = self.localState.player
        if player:
            lastAngle, lastThrust = self.lastPlayerAimSent
            if (
                    lastAngle != player.angleFacing or
                    lastThrust != player.ghostThrust):
                reactor.callLater(
                    0, self.game.agentRequest, self, AimPlayerAtMsg(
                        player.angleFacing, player.ghostThrust, tickId))
                self.lastPlayerAimSent = (
                    player.angleFacing, player.ghostThrust)

    @ResyncPlayerMsg.handler
    def handle_ResyncPlayerMsg(self, msg):
        oldKeyState = dict(self.localState.player._state)
        self.localState.player.applyPlayerUpdate(msg)
        self.resyncLocalPlayer(oldKeyState)

    def resyncLocalPlayer(self, oldKeyState):
        newKeyState = self.localState.player._state
        self.sendRequest(self.localState.player.buildResyncAcknowledgement())
        self.nextSyncCheck = self.world.lastTickId + SYNC_CHECK_PERIOD

        for key, value in oldKeyState.iteritems():
            if value != newKeyState[key]:
                self.sendRequest(UpdatePlayerStateMsg(
                    value, self.world.lastTickId, stateKey=key))

    @UpgradeApprovedMsg.handler
    def handle_UpgradeApprovedMsg(self, msg):
        self.sendRequest(PlayerHasUpgradeMsg(
            msg.upgradeType, self.world.lastTickId))

    def sendJoinRequest(self, teamId, nick, authTag=0, bot=False):
        if self.player is not None:
            raise RuntimeError('Already joined.')

        msg = JoinRequestMsg(
            teamId, authTag=authTag, nick=nick.encode(), bot=bot)
        if bot:
            msg.localBotRequest = True

        self.sendRequest(msg)


class LocalState(object):
    '''
    Stores state information which a client wants to keep which do not need to
    wait for a round trip to the server. e.g. when a player moves, it should
    start moving on the local screen even before the server has received the
    message.
    '''

    LOCAL_ID_CAP = 1 << 16

    def __init__(self, agent):
        self.agent = agent
        self.world = agent.world
        self.player = None
        self.onShoxwave = Event()
        self.shotById = {}
        self.localShots = {}
        self.localGrenade = None
        self.nextLocalId = 1
        self.serverDelay = INITIAL_ASSUMED_LATENCY
        self.world.onShotRemoved.addListener(self.shotRemoved)

    @property
    def shots(self):
        for shot in self.shotById.itervalues():
            yield shot
        for shot in self.localShots.itervalues():
            yield shot

    def playerJoined(self, player):
        # Create a shallow copy of the player object, and use it to simulate
        # movement before the server approves it.
        self.player = player.clone()

        player.onZombieHit.addListener(self.noticedZombieHit)
        player.onStarsChanged.addListener(self.playerStarsChanged)
        player.onGotTrosball.addListener(self.gotTrosball)
        player.onDied.addListener(self.died)

    def refreshPlayer(self):
        realPlayer = self.world.playerWithId[self.player.id]
        self.player.restore(realPlayer.dump())

    def noticedZombieHit(self, killer, shot, deathType):
        self.player.properHit(killer, deathType)

    def playerStarsChanged(self):
        if self.player.dead:
            return
        player = self.world.getPlayer(self.player.id)
        self.player.stars = player.stars

    def gotTrosball(self):
        self.player.deleteUpgrade()

    def died(self, killer, deathType):
        self.localShots.clear()

    def lostPlayer(self):
        self.player.onZombieHit.removeListener(self.noticedZombieHit)
        self.player.onStarsChanged.removeListener(self.playerStarsChanged)
        self.player.onGotTrosball.removeListener(self.gotTrosball)
        self.player.onDied.removeListener(self.died)
        self.player = None

    def shotFired(self):
        if self.player.shoxwave:
            self.onShoxwave()
            localId = 0
        else:
            localId = self.nextLocalId
            self.nextLocalId = (self.nextLocalId + 1) % self.LOCAL_ID_CAP
            self.localShots[localId] = self.player.createShot(
                shotClass=LocalShot)
        self.player.weaponDischarged()
        return localId

    def matchShot(self, localId, shotId):
        if localId in self.localShots:
            shot = self.localShots.pop(localId)
            shot.realShotStarted = True
            self.shotById[shotId] = shot

    def shotRemoved(self, shotId, *args, **kwargs):
        if shotId in self.shotById:
            del self.shotById[shotId]

    def grenadeLaunched(self):
        self.localGrenade = LocalGrenade(
            self, self.world, self.player, Grenade.timeRemaining)

    def matchGrenade(self):
        for grenade in self.world.grenades:
            if grenade.player.id == self.player.id:
                self.localGrenade.realShotStarted = True
                return

    def grenadeRemoved(self):
        self.localGrenade = None

    def tick(self):
        if self.player:
            self.player.reset()
            self.player.advance()

            if not self.player.dead:
                for unit in self.world.getCollectableUnits():
                    if unit.hitLocalPlayer:
                        continue
                    if unit.checkCollision(self.player, 0):
                        unit.collidedWithLocalPlayer(self.player)

        for shot in self.shotById.values() + self.localShots.values():
            shot.reset()
            shot.advance()
        if self.localGrenade:
            self.localGrenade.reset()
            self.localGrenade.advance()

        for shotId, shot in self.shotById.items():
            if shot.expired:
                del self.shotById[shotId]
        for localId, shot in self.localShots.items():
            if shot.expired:
                del self.localShots[localId]
