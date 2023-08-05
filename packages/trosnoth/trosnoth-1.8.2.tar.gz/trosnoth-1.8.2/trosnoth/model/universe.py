'''universe.py - defines anything that has to do with the running of the
universe. This includes players, shots, zones, and the level itself.'''

from collections import defaultdict
import functools
import heapq
import logging
from math import sin, cos
import random
import itertools

from twisted.internet import defer, reactor

from trosnoth.const import (
    TURRET_DEATH, TROSBALL_DEATH, SHOXWAVE_DEATH, STALEMATE_CHECK_PERIOD,
    COLLECTABLE_STAR_LIFETIME, NO_COLLECTABLE_STARS, TICK_PERIOD,
    MAX_PLAYER_NAME_LENGTH, ZONE_TAG_STAR_HALF_LIFE, GAME_STATE_CHECK_PERIOD,
    RABBIT_CHASING_PERIOD, BOMBER_DEATH,
)
from trosnoth.utils import globaldebug
from trosnoth.utils.math import distance
from trosnoth.model.idmanager import IdManager
from trosnoth.model.upgrades import upgradeOfType, allUpgrades
from trosnoth.model.physics import WorldPhysics

from trosnoth.model import gameStates
from trosnoth.model.map import MapLayout, MapState
from trosnoth.model.player import Player
from trosnoth.model.star import CollectableStar
from trosnoth.model.shot import Shot, GrenadeShot
from trosnoth.model.team import Team
from trosnoth.model.trosball import Trosball

from trosnoth.utils.event import Event
from trosnoth.utils.message import MessageConsumer
from trosnoth.utils.twist import WeakCallLater, WeakLoopingCall
from trosnoth.utils.unrepr import unrepr
from trosnoth.messages import (
    TaggingZoneMsg, ShotFiredMsg, RespawnMsg, ChatFromServerMsg,
    GameStartMsg, GameOverMsg, RemovePlayerMsg, ShotHitPlayerMsg,
    AddPlayerMsg, PlayerStarsSpentMsg, SetPlayerTeamMsg, WorldLoadingMsg,
    ZoneStateMsg, WorldResetMsg,
    CreateCollectableStarMsg, RemoveCollectableStarMsg, PlayerHasElephantMsg,
    FireShoxwaveMsg, UpgradeChangedMsg,
    PlayerHasTrosballMsg, TrosballPositionMsg, AwardPlayerStarMsg,
    TrosballTagMsg, ChangeTimeLimitMsg, StartingSoonMsg, TickMsg,
    ReturnToLobbyMsg, TICK_LIMIT,
)

log = logging.getLogger('universe')


class DelayedCall(object):
    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False

    def cancel(self):
        self.cancelled = True



class UnknownMapLayouts(Exception):
    def __init__(self, *args, **kwargs):
        super(UnknownMapLayouts, self).__init__(*args, **kwargs)
        self.keys = self.message


class Timer(object):
    def __init__(self, world):
        self.world = world
        self.duration = 0
        self.gameStartingIn = -1
        self.gameStartDelay = -1
        self.gameOverTime = None
        self.elapsedTime = 0.0

        self.onGameStart = Event()

    def setMatchDuration(self, duration):
        self.duration = duration

    def getMatchDuration(self):
        return self.duration

    def hasTimeLimit(self):
        if not self.world.state.isTimedGameState():
            return False
        return self.duration != 0

    def getTimeLeft(self):
        '''
        Return the amount of time left on the clock. If the game is over, the
        clock may be stopped at the figure it was on when the game finished.
        If the game is untimed, may return 0.
        '''
        gameTimeMode = self.world.state.getGameTimeMode()
        if gameTimeMode == 'unstarted':
            return self.duration
        if self.duration == 0:
            # Untimed game
            return 0
        if gameTimeMode == 'running':
            return self.duration - self.getElapsedTime()
        if gameTimeMode == 'ended':
            return self.duration - self.gameOverTime

    def dumpState(self):
        return {
            'timeRunning': self.getElapsedTime(),
            'timeLimit': self.duration,
        }

    def restoreState(self, data):
        self.duration = data['timeLimit']
        self.elapsedTime = data['timeRunning']

    def tick(self):
        if self.gameStartingIn > 0:
            self.gameStartingIn -= TICK_PERIOD
            if self.gameStartingIn <= 0:
                self.onGameStart()
                self.onGameStart = Event()

        self.elapsedTime += self.world.tickPeriod

    def beginGameStartCountdown(self, delay):
        self.gameStartingIn = delay
        self.gameStartDelay = delay

    def getStartCountdown(self):
        return self.gameStartingIn

    def getStartCountdownMax(self):
        return self.gameStartDelay

    def gameFinishedNow(self):
        self.gameOverTime = self.getElapsedTime()

    def getElapsedTime(self):
        return self.elapsedTime

    def reset(self):
        self.elapsedTime = 0.0


class Abilities(object):
    def __init__(self):
        self.upgrades = True
        self.respawn = True
        self.leaveFriendlyZones = True
        self.zoneCaps = True
        self.stars = True


class UIOptions(object):
    '''
    Represents options related to how this kind of match should be displayed to
    the user.
    '''

    def __init__(self):
        self.showNets = False
        self.shiftingFrontLine = False
        self.frontLineGetter = None
        self.showWinner = False
        self.showReadyStates = False


class StarSpawner(object):
    def __init__(self, world):
        self.world = world

        self._lastStalemateCheck = 0.0
        self.lastZoneTagged = 0.0

        self.world.onZoneTagged.addListener(self.zoneTagged)

    def stop(self):
        self.world.onZoneTagged.removeListener(self.zoneTagged)

    def reset(self):
        self._lastStalemateCheck = 0.0
        self.lastZoneTagged = 0.0

    def zoneTagged(self, *args, **kwargs):
        self.lastZoneTagged = self.world.timer.getElapsedTime()

    def collectableStarsCanAppear(self):
        if NO_COLLECTABLE_STARS:
            return False
        if not self.world.abilities.stars:
            return False
        return True

    def tick(self):
        if not self.collectableStarsCanAppear():
            return

        now = self.world.timer.getElapsedTime()
        if now < self._lastStalemateCheck + STALEMATE_CHECK_PERIOD:
            return
        self._lastStalemateCheck = now

        prob = 0.5 ** ((now - self.lastZoneTagged) / ZONE_TAG_STAR_HALF_LIFE)
        if random.random() > prob:
            # Distribute the stars evenly by team
            team = random.choice(self.world.teams)
            zone = self.world.selectZoneForTeam(team.id)
            if zone.owner != team:
                return
            x, y = zone.defn.randomPosition()
            starId = self.world.idManager.newStarId()
            if starId is not None:
                self.world.sendServerCommand(
                    CreateCollectableStarMsg(starId, x, y))



class Universe(MessageConsumer):
    '''Universe(halfMapWidth, mapHeight)
    Keeps track of where everything is in the level, including the locations
    and states of every alien, the terrain positions, and who owns the
    various territories and orbs.'''

    PLAYER_RESET_STARS = 0

    isServer = False

    def __init__(
            self, layoutDatabase, halfMapWidth=3, mapHeight=2,
            authTagManager=None, duration=0, onceOnly=False):
        '''
        halfMapWidth:   is the number of columns of zones in each team's
                        territory at the start of the game. There will always
                        be a single column of neutral zones between the two
                        territories at the start of the game.
        mapHeight:      is the number of zones in every second column of
                        zones. Every other column will have mapHeight + 1
                        zones in it. This is subject to the constraints that
                        (a) the columns at the extreme ends of the map will
                        have mapHeight zones; (b) the central (initially
                        neutral) column of zones will never have fewer zones
                        in it than the two bordering it - this will sometimes
                        mean that the column has mapHeight + 2 zones in it.
        '''
        super(Universe, self).__init__()

        self.onPlayerAdded = Event()        # (player)
        self.onPlayerRemoved = Event()      # (player, oldId)
        self.onGameStateChanged = Event()
        self.onTeamScoreChanged = Event()
        self.onShotRemoved = Event()        # (shotId)
        self.onCollectableStarRemoved = Event()
        self.onSectorNeutralised = Event()  # (tagger, zoneCount)
        self.onGameOver = Event()           # (team, timeOver)
        self.onZoneTagged = Event()         # (zone, player, previousOwner)
        self.onOpenChatReceived = Event()   # (text, sender)
        self.onTeamChatReceived = Event()   # (team, text, sender)
        self.onPlayerKill = Event()         # (killer, target, deathType)
        self.onPlayerRespawn = Event()      # (player)
        self.onGrenadeExplosion = Event()   # (pos, radius)
        self.onTrosballExplosion = Event()  # (player)
        self.onBomberExplosion = Event()    # (player)
        self.onReset = Event()
        self.onServerTickComplete = Event()
        self.onChangeVoiceChatRooms = Event()   # (teams, players)

        self.delayedCalls = []

        self.isIncomplete = False
        self.playerWithElephant = None
        self.physics = WorldPhysics(self)
        if authTagManager is None:
            self.authManager = None
        else:
            self.authManager = authTagManager.authManager

        self.playerWithId = {}
        self.shotWithId = {}
        self.teamWithId = {'\x00': None}

        self.trosballScore = {'A': 0, 'B': 0}

        # Create Teams:
        self.teams = (
            Team(self, 'A'),
            Team(self, 'B'),
        )
        Team.setOpposition(self.teams[0], self.teams[1])

        for t in self.teams:
            self.teamWithId[t.id] = t

        # Set up zones
        self.zoneWithDef = {}
        self.layout = MapLayout(halfMapWidth, mapHeight)
        self.map = MapState(self, self.layout)
        self.zoneWithId = self.map.zoneWithId
        self.zones = self.map.zones
        self.zoneBlocks = self.map.zoneBlocks

        self.players = set()
        self.grenades = set()
        self.collectableStars = {}      # starId -> CollectableStar
        self.trosball = None
        self.deadStars = set()
        self.trosballPlayer = None
        self.trosballCooldownPlayer = None
        self.playerGotTrosballTime = None
        self.gameMode = 'Normal'
        self.rogueTeamName = 'Rogue'
        self.tickPeriod = TICK_PERIOD
        self._gameSpeed = 1.0
        self._gameInProgress = False
        self._winningTeam = None
        self.lastTickId = 0
        self.loading = False

        self.layoutDatabase = layoutDatabase
        self._onceOnly = onceOnly
        self.timer = Timer(self)
        self.timer.setMatchDuration(duration)
        self.abilities = Abilities()
        self.uiOptions = UIOptions()

        self.loadedMap = None

        self.setGameState(gameStates.Lobby)
        self._nextGameStateCheck = self.timer.getElapsedTime()

    def isValidNick(self, nick):
        if len(nick) < 2 or len(nick) > MAX_PLAYER_NAME_LENGTH:
            return False
        return True

    @property
    def shots(self):
        '''
        Used by UI to iterate through shots.
        '''
        return self.shotWithId.itervalues()

    def defaultHandler(self, msg):
        msg.applyOrderToWorld(self)

    def selectZoneForTeam(self, teamId):
        '''
        Randomly selects a zone, giving preference to:
            1. Zones owned by the given team that are adjacent to an enemy zone
            2. Zones owned by the given team that are adjacent to a zone not
                owned by the team.
            3. Other zones owned by the given team.
            4. Other zones.
        '''
        team = self.getTeam(teamId)
        allTeamZones = [
            z for z in self.map.zones
            if z.owner is not None and z.owner.id == teamId]
        nextToEnemy = []
        nextToNeutral = []
        for zone in list(allTeamZones):
            enemy = neutral = False
            for adjDef in zone.defn.adjacentZones.iterkeys():
                if adjDef is None:
                    continue
                adj = self.zoneWithDef[adjDef]
                if adj.owner is None:
                    neutral = True
                elif adj.isEnemyTeam(team):
                    enemy = True
            if enemy:
                nextToEnemy.append(zone)
            elif neutral:
                nextToNeutral.append(zone)

        return random.choice(
            nextToEnemy
            or nextToNeutral
            or allTeamZones
            or list(self.map.zones))

    @WorldResetMsg.handler
    def gotWorldReset(self, msg):
        if not self.isServer:
            data = unrepr(msg.settings)
            self.restoreEverything(data)

        self.timer.reset()
        self._nextGameStateCheck = GAME_STATE_CHECK_PERIOD

    def getTeam(self, teamId):
        if teamId == '\x00':
            return None
        return self.teamWithId[teamId]

    def getPlayer(self, playerId, default=None):
        return self.playerWithId.get(playerId, default)

    def getUpgradeType(self, upgradeTypeId):
        return upgradeOfType[upgradeTypeId]

    def getZone(self, zoneId, default=None):
        return self.map.zoneWithId.get(zoneId, default)

    def getShot(self, sId):
        return self.shotWithId[sId]

    def setGameMode(self, mode):
        if self.physics.setMode(mode):
            self.gameMode = mode
            log.debug('Client: GameMode is set to ' + mode)

    def setGameSpeed(self, speed):
        '''Sets the speed of the game to a proportion of normal speed.
        That is, speed=2.0 is twice as fast a game as normal
        '''
        self._gameSpeed = speed
        self.tickPeriod = TICK_PERIOD * speed

    @GameOverMsg.handler
    def gameOver(self, msg):
        self._nextGameStateCheck = (
            self.timer.getElapsedTime() + RABBIT_CHASING_PERIOD)
        self.setWinningTeamById(msg.teamId)
        self.timer.gameFinishedNow()
        self.setGameState(gameStates.Ended)

        self.onGameOver(self.getTeam(msg.teamId), msg.timeOver)

        for player in self.players:
            player.readyToStart = False
            player.readyForTournament = False

        self._gameInProgress = False

    def gameIsInProgress(self):
        return self._gameInProgress

    @GameStartMsg.handler
    def gameStart(self, msg):
        self.setGameState(self.state.getInProgressState())
        self.timer.reset()
        self._gameInProgress = True
        for team in self.teams:
            team.resetScore()

    @AddPlayerMsg.handler
    def handle_AddPlayerMsg(self, msg):
        team = self.teamWithId[msg.teamId]
        zone = self.zoneWithId[msg.zoneId]

        # Create the player.
        nick = msg.nick.decode()
        player = Player(self, nick, team, msg.playerId, msg.dead, msg.bot)
        player.teleportToZoneCentre(zone)
        player.resyncBegun()

        self.addPlayer(player)

    def addPlayer(self, player):
        # Add this player to this universe.
        self.players.add(player)
        self.playerWithId[player.id] = player
        self.onPlayerAdded(player)

    @PlayerHasElephantMsg.handler
    def gotElephantMsg(self, msg):
        player = self.getPlayer(msg.playerId)
        self.playerWithElephant = player

    @PlayerHasTrosballMsg.handler
    def handle_PlayerHasTrosballMsg(self, msg):
        self.setTrosballPlayer(self.playerWithId[msg.playerId])

    def setTrosballPlayer(self, player):
        self.trosballPlayer = player
        self.trosballPlayer.deleteUpgrade()
        self.playerGotTrosballTime = self.timer.getElapsedTime()
        self.trosball = None
        self.trosballPlayer.onGotTrosball()

    @TrosballPositionMsg.handler
    def handle_TrosballPositionMsg(self, msg):
        self.setTrosballPosition((msg.xpos, msg.ypos), (msg.xvel, msg.yvel))

    def setTrosballPosition(self, pos, vel):
        self.trosballPlayer = None
        if self.trosball is None:
            self.trosball = Trosball(self)
        self.trosball.teleport(pos, vel[0], vel[1])

    @TrosballTagMsg.handler
    def handle_TrosballTagMsg(self, msg):
        self.setGameState(gameStates.BetweenTrosballPoints)
        if msg.teamId == '\x00':
            return
        self.trosballScore[msg.teamId] += 1
        self.trosballPlayer = None
        winningTeam = self.teamWithId[msg.teamId]
        netPosition = self.getTrosballTargetZoneDefn(winningTeam).pos
        if self.trosball is None:
            self.trosball = Trosball(self)
        self.trosball.setIsInNet(netPosition)

    def teamsWithHighestTrosballScore(self):
        maxScore = max(self.trosballScore.itervalues())
        return [
            self.teamWithId[teamId]
            for teamId, score in self.trosballScore.iteritems()
            if score == maxScore]

    def delPlayer(self, player):
        playerId = player.id
        player.removeFromGame()
        self.players.remove(player)
        del self.playerWithId[player.id]
        if player == self.playerWithElephant:
            self.returnElephantToOwner()

        # In case anyone else keeps a reference to it
        player.id = -1
        self.onPlayerRemoved(player, playerId)

    def advanceEverything(self):
        '''Advance the state of the game by deltaT seconds'''

        for shot in list(self.shots):
            if shot.expired:
                del self.shotWithId[shot.id]
                self.onShotRemoved(shot.id)

        # Update the player and shot positions.
        advancables = (
            self.shotWithId.values() + list(self.players) + list(self.grenades)
            + self.collectableStars.values())
        if self.trosball is not None:
            advancables.append(self.trosball)
        for unit in advancables:
            unit.reset()
            unit.advance()

        self.updateZoneInhabitants(advancables)

        if self.state.isTrosball():
            self.updateTrosballZones()

            if self.trosballPlayer is not None:
                if (self.timer.getElapsedTime() - self.playerGotTrosballTime >=
                        self.physics.trosballExplodeTime):
                    self.explodeTrosball()

    def getCollectableUnits(self):
        for star in self.collectableStars.values():
            yield star
        if self.trosball:
            yield self.trosball
        for unit in list(self.deadStars):
            yield unit

    def updateZoneInhabitants(self, advancables):
        for zone in self.map.zones:
            zone.clearPlayers()
        for unit in advancables:
            if isinstance(unit, Player):
                zone = unit.getZone()
                if zone:
                    zone.addPlayer(unit)

    def explodeTrosball(self):
        assert self.trosballPlayer is not None
        player = self.trosballPlayer
        player.killOutright(deathType=TROSBALL_DEATH)
        self.onTrosballExplosion(player)

    def updateTrosballZones(self):
        if self.state.isTrosball():
            try:
                trosballPosition = self.getTrosballPosition()
            except ValueError:
                pass
            else:
                for zone in self.zones:
                    # Don't update target zones:
                    if not any([
                            self.getTrosballTargetZoneDefn(team) ==
                            zone.defn for team in self.teams]):
                        zone.updateByTrosballPosition(trosballPosition)

    def bomberExploded(self, player):
        player.killOutright(deathType=BOMBER_DEATH, resync=False)
        self.onBomberExplosion(player)

    def canShoot(self):
        return self.physics.shooting and self.state.canShoot()

    def canRename(self):
        return self.state.canRename()

    def setWinningTeamById(self, teamId):
        self._winningTeam = self.teamWithId.get(teamId, None)

    def getWinningTeam(self):
        return self._winningTeam

    @CreateCollectableStarMsg.handler
    def createCollectableStar(self, msg):
        self.addCollectableStar(
            CollectableStar(self, msg.starId, (msg.xPos, msg.yPos)))

    @RemoveCollectableStarMsg.handler
    def gotRemoveCollectableStarMsg(self, msg):
        # On the server, the star must be remembered in case a player is about
        # to collect it but we don't know yet.
        if not self.isServer:
            del self.collectableStars[msg.starId]
            self.onCollectableStarRemoved(msg.starId)

    def teamWithAllZones(self):
        # Now check for an all zones win.
        team2Wins = self.teams[0].isLoser()
        team1Wins = self.teams[1].isLoser()
        if team1Wins and team2Wins:
            # The extraordinarily unlikely situation that all
            # zones have been neutralised in the same tick
            return 'Draw'
        elif team1Wins:
            return self.teams[0]
        elif team2Wins:
            return self.teams[1]
        else:
            return None

    def teamWithMoreZones(self):
        if self.teams[0].numZonesOwned > self.teams[1].numZonesOwned:
            return self.teams[0]
        elif self.teams[1].numZonesOwned > self.teams[0].numZonesOwned:
            return self.teams[1]
        else:
            return None

    def getTeamPlayerCounts(self):
        '''
        Returns a mapping from team id to number of players currently on that
        team.
        '''
        playerCounts = {}
        for player in self.players:
            playerCounts[player.teamId] = playerCounts.get(
                player.teamId, 0) + 1
        return playerCounts

    def getTeamToJoin(self, preferredTeamId):
        return self.state.getTeamToJoin(preferredTeamId, self)

    def getTeamName(self, id):
        if id == '\x00':
            return self.rogueTeamName
        return self.getTeam(id).teamName

    @FireShoxwaveMsg.handler
    def shoxwaveExplosion(self, msg):
        radius = 128
        # Get the player who fired this shoxwave
        shoxPlayer = self.getPlayer(msg.playerId)
        if not shoxPlayer:
            return
        shoxPlayer.weaponDischarged()

        # Loop through all the players in the game
        for player in self.players:
            if not (player.isFriendsWith(shoxPlayer) or distance(player.pos,
                    shoxPlayer.pos) > radius or player.dead or
                    player.isInvulnerable() or
                    player.phaseshift or player.turret):
                player.zombieHit(shoxPlayer, None, SHOXWAVE_DEATH)

        for shot in self.shotWithId.values():
            if (not shot.originatingPlayer.isFriendsWith(shoxPlayer) and
                    distance(shot.pos, shoxPlayer.pos) <= radius):
                shot.expired = True

    @ShotFiredMsg.handler
    def shotFired(self, msg):
        '''A player has fired a shot.'''
        try:
            player = self.playerWithId[msg.playerId]
        except KeyError:
            return

        shot = player.createShot(msg.shotId)
        self.shotWithId[msg.shotId] = shot
        player.weaponDischarged()
        player.onShotFired(shot)

    def _killTurret(self, tagger, zone):
        if zone.turretedPlayer is not None:
            zone.turretedPlayer.killOutright(
                deathType=TURRET_DEATH, killer=tagger)

    def trosballLost(self, formerOwner):
        self.setTrosballPosition(
            formerOwner.pos, formerOwner.getCurrentVelocity())

    @TaggingZoneMsg.handler
    def zoneTagged(self, msg):
        if msg.playerId == '\x00':
            player = None
        else:
            player = self.playerWithId[msg.playerId]
        zone = self.map.zoneWithId[msg.zoneId]
        previousOwner = zone.owner
        zone.tag(player)
        self._killTurret(player, zone)
        self.onZoneTagged(zone, player, previousOwner)
        if player:
            player.onTaggedZone(zone, previousOwner)

    @ZoneStateMsg.handler
    def zoneOwned(self, msg):
        zone = self.map.zoneWithId[msg.zoneId]
        team = self.teamWithId[msg.teamId]
        zone.setOwnership(team, msg.dark)

    @RespawnMsg.handler
    def respawn(self, msg):
        player = self.getPlayer(msg.playerId)
        zone = self.getZone(msg.zoneId)
        if player and zone:
            player.respawn(zone)

    @PlayerStarsSpentMsg.handler
    def starsSpent(self, msg):
        player = self.getPlayer(msg.playerId)
        if player:
            player.stars -= msg.count
            player.onStarsChanged()

    @UpgradeChangedMsg.handler
    def changeUpgrade(self, msg):
        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == msg.upgradeType:
                if msg.statType == 'S':
                    upgradeClass.requiredStars = msg.newValue
                elif msg.statType == 'T':
                    upgradeClass.timeRemaining = msg.newValue
                elif msg.statType == 'E':
                    upgradeClass.enabled = bool(msg.newValue)

    def addGrenade(self, grenade):
        self.grenades.add(grenade)

    def removeGrenade(self, grenade):
        self.grenades.remove(grenade)

    def addCollectableStar(self, star):
        self.collectableStars[star.id] = star

    def setGameState(self, state):
        # Reset abilities and ui options
        self.abilities = Abilities()
        self.uiOptions = UIOptions()

        self.state = state
        self.state.applyTo(self)
        self.onGameStateChanged()
        self.state.onBecomingCurrentState(self)

    def getTeamStars(self, team):
        if team is None:
            return 0
        total = 0
        for p in self.players:
            if p.team == team:
                total += p.stars
        return total

    def getTrosballPosition(self):
        if self.trosball:
            return self.trosball.pos
        elif self.trosballPlayer:
            return self.trosballPlayer.pos
        elif self.state.isTrosball():
            # Game probably hasn't started yet, assume the middle.
            return (self.map.layout.centreX, self.map.layout.centreY)
        else:
            raise ValueError('no Trosball')

    def getTrosballTargetZoneDefn(self, team):
        return self.layout.getTrosballTargetZoneDefn(team)

    def setLayout(self, layout):
        self.zoneWithDef = {}
        for team in self.teams:
            team.numZonesOwned = 0
        self.layout = layout
        self.map = MapState(self, self.layout)
        self.zoneWithId = self.map.zoneWithId
        self.zones = self.map.zones
        self.zoneBlocks = self.map.zoneBlocks

    def setTestMode(self):
        self.PLAYER_RESET_STARS = 20
        for upgradetype in allUpgrades:
            upgradetype.requiredStars = 1

    def isTournamentTeam(self, teamName):
        if not self.authManager:
            return False
        return teamName in self.authManager.tournamentSettings.teamNames

    def getStartingGameStateFromString(self, gameType):
        if gameType == 'normal':
            return gameStates.Starting
        if gameType == 'trosball':
            return gameStates.StartingTrosball
        if gameType == 'solotrosball':
            return gameStates.StartingSoloTrosball
        if gameType == 'solo':
            return gameStates.StartingSolo
        raise ValueError('unknown game type %r', gameType)

    @TickMsg.handler
    def tickReceived(self, msg):
        self.timer.tick()
        self.advanceEverything()
        self.lastTickId = msg.tickId

        self.processDelayedCalls()

    def processDelayedCalls(self):
        now = self.timer.getElapsedTime()
        while self.delayedCalls:
            if self.delayedCalls[0][0] > now:
                break
            when, call = heapq.heappop(self.delayedCalls)
            if call.cancelled:
                continue
            try:
                call.fn(*call.args, **call.kwargs)
            except Exception:
                log.exception('Error in delayed call')

    @StartingSoonMsg.handler
    def startingSoon(self, msg):
        self.timer.beginGameStartCountdown(msg.delay)
        gameState = self.getStartingGameStateFromString(msg.gameType)
        self.setGameState(gameState)

    @ReturnToLobbyMsg.handler
    def returnToLobby(self, msg):
        self.lobbyTeamIds = {}
        self.setGameState(gameStates.Lobby)
        self._nextGameStateCheck = (
            self.timer.getElapsedTime() + GAME_STATE_CHECK_PERIOD)
        log.debug('Returning to lobby')

    def dumpEverything(self):
        '''Returns a dict representing the settings which must be sent to
        clients that connect to this server.'''

        result = {
            'loading': self.loading,
            'teams': [
                {
                    'id': team.id,
                    'name': team.teamName,
                    'trosballScore': self.trosballScore[team.id]
                        if self.state.isTrosball() else None,
                } for team in self.teams
            ],
            'worldMap': self.map.layout.toString(),
            'mode': self.gameMode,
            'state': self.state.id,
            'timer': self.timer.dumpState(),
            'speed': self._gameSpeed,
            'zones': [
                {
                    'id': zone.id,
                    'teamId': zone.owner.id if zone.owner else '\x00',
                    'dark': zone.dark,
                } for zone in self.zones
            ],
            'players': [player.dump() for player in self.players],
            'trosball': {
                'pos': self.trosball.pos if self.trosball else None,
                'vel': [self.trosball.xVel, self.trosball.yVel]
                    if self.trosball else None,
                'playerId': self.trosballPlayer.id
                    if self.trosballPlayer else None,
                'catchTime': self.playerGotTrosballTime
                    if self.trosballPlayer else None,
            } if self.trosball or self.trosballPlayer else None,
            'upgrades': [
                {
                    'type': upgrade.upgradeType,
                    'cost': upgrade.requiredStars,
                    'time': upgrade.timeRemaining,
                    'enabled': upgrade.enabled,
                } for upgrade in allUpgrades
            ],
            'elephant': self.playerWithElephant.id
                if self.playerWithElephant else None,
            'shots': [
                {
                    'id': shot.id,
                    'team': shot.team.id if shot.team else '\x00',
                    'pos': shot.pos,
                    'vel': shot.vel,
                    'shooter': shot.originatingPlayer.id,
                    'time': shot.timeLeft,
                    'kind': shot.kind,
                } for shot in self.shotWithId.itervalues() if not shot.expired
            ],
            'stars': [
                {
                    'id': star.id,
                    'created': star.creationTime,
                    'pos': star.pos,
                    'xVel': star.xVel,
                    'yVel': star.yVel,
                } for star in self.collectableStars.itervalues()
            ],
            'grenades': [
                {
                    'player': grenade.player.id if grenade.player else '\x00',
                    'pos': grenade.pos,
                    'xVel': grenade.xVel,
                    'yVel': grenade.yVel,
                    'timeLeft': grenade.timeLeft,
                } for grenade in self.grenades
            ],
            'physics': self.physics.dumpState(),
            'lastTickId': self.lastTickId,
        }

        return result

    def restoreEverything(self, data):
        self.loading = data['loading']
        if 'lastTickId' in data:
            self.lastTickId = data['lastTickId']

        for teamData in data['teams']:
            teamId = teamData['id']
            self.teamWithId[teamId].teamName = teamData['name']
            if teamData['trosballScore'] is not None:
                self.trosballScore[teamId] = teamData['trosballScore']

        gameState = gameStates.gameStatesById[data['state']]
        self.setGameState(gameState)
        self.timer.restoreState(data['timer'])
        self.physics.restoreState(data['physics'])

        mapSpec = data['worldMap']
        keys = MapLayout.unknownBlockKeys(self.layoutDatabase, mapSpec)
        if keys:
            # We don't know all of the map blocks, so there is no point
            # proceeding.
            self.isIncomplete = True
            self.onReset()
            raise UnknownMapLayouts(keys)

        layout = MapLayout.fromString(self.layoutDatabase, mapSpec)
        self.setLayout(layout)

        self.setGameMode(data['mode'])
        self.setGameSpeed(data['speed'])

        for zoneData in data['zones']:
            self.getZone(zoneData['id']).setOwnership(
                self.teamWithId[zoneData['teamId']], zoneData['dark'])

        for playerData in data['players']:
            playerId = playerData['id']
            team = self.teamWithId[playerData['teamId']]
            nick = playerData['nick']

            if playerId in self.playerWithId:
                player = self.playerWithId[playerId]
            else:
                player = Player(self, nick, team, playerId)
                self.addPlayer(player)

            player.restore(playerData)

        trosball = data['trosball']
        if trosball:
            if trosball['playerId']:
                self.setTrosballPlayer(
                    self.getPlayer(trosball['playerId']))
                self.playerGotTrosballTime = trosball['catchTime']
            elif trosball['pos']:
                self.setTrosballPosition(trosball['pos'], trosball['vel'])

        for upgradeData in data['upgrades']:
            for upgradeClass in allUpgrades:
                if upgradeClass.upgradeType == upgradeData['type']:
                    upgradeClass.requiredStars = upgradeData['cost']
                    upgradeClass.timeRemaining = upgradeData['time']
                    upgradeClass.enabled = upgradeData['enabled']

        self.playerWithElephant = self.getPlayer(data['elephant'])

        self.shotWithId = {}
        for shotData in data['shots']:
            shot = Shot(
                self, shotData['id'], self.getTeam(shotData['team']),
                self.getPlayer(shotData['shooter']), tuple(shotData['pos']),
                tuple(shotData['vel']), shotData['kind'], shotData['time'])
            self.shotWithId[shot.id] = shot

        self.deadStars = set()
        self.collectableStars = {}
        for starData in data['stars']:
            star = CollectableStar(
                self, starData['id'], tuple(starData['pos']))
            star.creationTime = starData['created']
            star.xVel = starData['xVel']
            star.yVel = starData['yVel']
            self.collectableStars[star.id] = star

        self.grenades = set()
        for grenadeData in data['grenades']:
            grenade = GrenadeShot(
                self, self.getPlayer(grenadeData['player']),
                grenadeData['timeLeft'])
            grenade.pos = grenadeData['pos']
            grenade.xVel = grenadeData['xVel']
            grenade.yVel = grenadeData['yVel']
            self.addGrenade(grenade)

        self.isIncomplete = False
        self.onReset()

    def canVote(self):
        return self.state == gameStates.Lobby and not self._onceOnly

    @ChangeTimeLimitMsg.handler
    def changeTimeLimit(self, msg):
        self.timer.setMatchDuration(msg.timeLimit)

    def resetTrosballToCentreOfMap(self):
        pass

    def elephantKill(self, killer):
        pass

    def playerHasNoticedDeath(self, player, killer):
        pass

    def stop(self):
        pass

    def callLater(self, _delay, _fn, *args, **kwargs):
        '''
        Schedules the given function to be called at the given game time.
        '''
        now = self.timer.getElapsedTime()
        heapq.heappush(
            self.delayedCalls, (now + _delay, DelayedCall(_fn, args, kwargs)))


class ServerUniverse(Universe):
    '''
    A universe that contains a few extra functions that are only needed
    server-side.
    '''

    isServer = True

    def __init__(self, game, *args, **kwargs):
        super(ServerUniverse, self).__init__(*args, **kwargs)
        self.game = game
        self.idManager = IdManager(self)
        self.starSpawner = StarSpawner(self)
        self._lastTickId = 0
        self.nextGameType = 'normal'
        self._loop = None
        self._startClock()

        reactor.callLater(0, self.loadPathFindingData)

        if __debug__ and globaldebug.enabled:
            globaldebug.serverUniverse = self

    @defer.inlineCallbacks
    def loadPathFindingData(self):
        from trosnoth.ais.pathfinding import RunTimePathFinder

        if self.map.layout.pathFinder:
            # Map has not changed since last load of data
            return

        self.sendServerCommand(WorldLoadingMsg(True))

        self.map.layout.pathFinder = RunTimePathFinder(self.map.layout)
        yield self.map.layout.pathFinder.loadData()
        self.sendServerCommand(WorldLoadingMsg(False))

    def needsPathFindingData(self, modeString):
        state = self.getStartingGameStateFromString(modeString)
        return state.aisEnabled()

    def sendServerCommand(self, msg):
        self.game.sendServerCommand(msg)

    def advanceEverything(self):
        super(ServerUniverse, self).advanceEverything()

        self.checkShotCollisions()
        self.updateZoneOwnership()
        self.starSpawner.tick()
        self.updateCollectableStars()
        for unit in list(self.deadStars):
            unit.beat()
            if not unit.history:
                self.deadStars.remove(unit)
                self.onCollectableStarRemoved(unit.id)
        for player in list(self.players):
            if player.resyncing and self.lastTickId > player.resyncExpiry:
                log.warning('%s took too long to resync', player)
                if player.agent:
                    player.agent.messageToAgent(ChatFromServerMsg(
                        error=True, text='You have been removed from the game '
                        'because your connection is too slow!'))
                self.sendServerCommand(RemovePlayerMsg(player.id))

    def checkShotCollisions(self, resolution=200):
        '''
        Performs collision checks of all shots with all nearby players.
        '''
        buckets = defaultdict(list)
        for player in self.players:
            if player.dead:
                continue
            x, y = player.pos
            xBucket, yBucket = x // resolution, y // resolution
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    buckets[xBucket + dx, yBucket + dy].append(player)

        for shot in list(self.shots):
            x, y = shot.pos
            xBucket, yBucket = x // resolution, y // resolution
            hitPlayers = [
                p for p in buckets[xBucket, yBucket]
                if shot.checkCollision(p)]
            if hitPlayers:
                # If multiple players are hit in the same tick, the server
                # randomly selects one to die.
                self.sendServerCommand(
                    ShotHitPlayerMsg(random.choice(hitPlayers).id, shot.id))

    def updateZoneOwnership(self):
        try:
            if not self.state.isTrosball():
                if not self.abilities.zoneCaps:
                    return
                tagger = None
                for zone in self.zones:
                    result = zone.playerWhoTaggedThisZone()
                    if result is not None:
                        tagger, team = result
                        if tagger is None:
                            assert team is None
                            self.sendServerCommand(
                                TaggingZoneMsg(zone.id, '\x00', '\x00'))
                        else:
                            self.sendServerCommand(TaggingZoneMsg(
                                zone.id, tagger.id, tagger.team.id))

                self.neutraliseDisconnectedZones(tagger)
        except:
            log.error('Error in zone ownership check', exc_info=True)

    def neutraliseDisconnectedZones(self, tagger):
        seenZones = set()
        teamSectors = dict((team, []) for team in self.teams)
        for zone in self.zones:
            if zone in seenZones:
                continue
            if zone.isNeutral():
                seenZones.add(zone)
                continue
            sector = zone.getContiguousZones()
            teamSectors[zone.owner].append(sector)
            seenZones.update(sector)

        for team, sectors in teamSectors.iteritems():
            if len(sectors) > 1:
                self.removeSmallestSector(team, sectors)
                zonesToNeutralise = list(itertools.chain(*sectors))
                self.neutraliseZones(zonesToNeutralise)
                self.onSectorNeutralised(tagger, len(zonesToNeutralise))
                if tagger:
                    # If two teams tag the same zone at the same time, tagger
                    # can be None.
                    tagger.onNeutralisedSector(len(zonesToNeutralise))

    def neutraliseZones(self, zones):
        for zone in zones:
            self.sendServerCommand(TaggingZoneMsg(zone.id, '\x00', '\x00'))

    def removeSmallestSector(self, team, sectors):
        '''
        Accepts team and list of sectors, selects which one that team should
        keep, returns the rest.
        '''
        key = functools.partial(self.getSectorGoodnessKey, team)
        goodSector = max(sectors, key=key)
        sectors.remove(goodSector)

    def getSectorGoodnessKey(self, team, sector):
        '''
        Returns a key by which sectors can be sorted with sectors which should
        be kept sorted as maximum.
        '''
        livePlayerCount = 0
        deadPlayerCount = 0
        darkZoneCount = 0
        for zone in sector:
            for player in zone.players:
                if player.team == team:
                    if player.dead:
                        deadPlayerCount += 1
                    else:
                        livePlayerCount += 1
            if zone.isDark():
                darkZoneCount += 1

        return (len(sector), livePlayerCount, darkZoneCount, deadPlayerCount)

    def updateCollectableStars(self):
        try:
            for star in self.collectableStars.values():
                if (star.creationTime < self.timer.getElapsedTime() -
                        COLLECTABLE_STAR_LIFETIME):
                    star.removeDueToTime()
        except:
            log.error('Error updating collectable stars', exc_info=True)

    def sendTrosballCollect(self, player):
        msg = PlayerHasTrosballMsg(player.id)
        self.sendServerCommand(msg)

    def sendTrosballPosition(self, x, y, xVel, yVel):
        msg = TrosballPositionMsg(x, y, xVel, yVel)
        self.sendServerCommand(msg)

    def resetTrosballToCentreOfMap(self):
        layout = self.map.layout
        x, y = (layout.centreX, layout.centreY)
        self.sendTrosballPosition(x, y, 0, 0)

    def throwTrosball(self):
        player = self.trosballPlayer
        xVel, yVel = player.getCurrentVelocity()
        angle = player.angleFacing
        xVel += self.physics.trosballThrowVel * sin(angle)
        yVel += -self.physics.trosballThrowVel * cos(angle)
        self.trosballCooldownPlayer = player

        WeakCallLater(0.2, self, 'clearTrosballCooldown', player)
        self.sendTrosballPosition(player.pos[0], player.pos[1], xVel, yVel)

    def clearTrosballCooldown(self, player):
        if self.trosballCooldownPlayer == player:
            self.trosballCooldownPlayer = None

    def returnElephantToOwner(self):
        for p in self.players:
            if p.isElephantOwner():
                self.sendServerCommand(PlayerHasElephantMsg(p.id))
                return
        self.sendServerCommand(PlayerHasElephantMsg('\x00'))

    def elephantKill(self, killer):
        if not killer.dead:
            self.sendServerCommand(PlayerHasElephantMsg(killer.id))
        else:
            self.returnElephantToOwner()

    def playerHasNoticedDeath(self, player, killer):
        if self.state.becomeNeutralWhenDie():
            if player.team is not None:
                self.sendServerCommand(SetPlayerTeamMsg(player.id, '\x00'))

        if killer and not killer.dead:
            self.sendServerCommand(AwardPlayerStarMsg(killer.id))

    @GameOverMsg.handler
    def gameOver(self, msg):
        super(ServerUniverse, self).gameOver(msg)

        for player in self.players:
            if player.dead and player.team is not None:
                self.sendServerCommand(SetPlayerTeamMsg(player.id, '\x00'))

    def _startGame(self, duration, size, delay=10):
        if self.loadedMap:
            layout = self.loadedMap
            self.loadedMap = None
        else:
            layout = self.layoutDatabase.generateRandomMapLayout(
                size[0], size[1])

        if duration is not None:
            self.timer.setMatchDuration(duration)
        self.setLayout(layout)

        self.beginGameStartCountdown(delay)

    def beginGameStartCountdown(self, delay=10):
        for player in self.players:
            zone = self.selectZoneForTeam(player.teamId)
            player.teleportToZoneCentre(zone)
            player.health = 0
            player.zombieHits = 0
            player.upgrade = None
            player._setStarsForDeath()
            player.respawnGauge = 0.0
            player.resyncBegun()

        self.trosballPlayer = None

        if self.state.isTrosball():
            self.trosball = Trosball(self)

        self.syncEverything()
        if self.needsPathFindingData(self.nextGameType):
            # By not yielding, we start the loading process and it continues on
            # its own
            self.loadPathFindingData()

        self.game.sendServerCommand(StartingSoonMsg(delay, self.nextGameType))

        self.callLater(delay, self.game.sendServerCommand, GameStartMsg())

    def syncEverything(self):
        self.game.sendServerCommand(WorldResetMsg(repr(self.dumpEverything())))

    def tick(self):
        if self.loading or len(self.players) == 0:
            return
        tickId = self._lastTickId = (self._lastTickId + 1) % TICK_LIMIT
        self.game.sendServerCommand(TickMsg(tickId))
        self.onServerTickComplete()

    def _startClock(self):
        if self._loop is not None:
            self._loop.stop()
        self._loop = WeakLoopingCall(self, 'tick')
        if __debug__ and globaldebug.enabled:
            self._loop.start(TICK_PERIOD * globaldebug.slowMotionFactor, False)
        else:
            self._loop.start(TICK_PERIOD, False)

    def _stopClock(self):
        if self._loop is not None:
            self._loop.stop()
            self._loop = None

    def stop(self):
        super(ServerUniverse, self).stop()
        self._stopClock()
        self.starSpawner.stop()

    @StartingSoonMsg.handler
    def startingSoon(self, msg):
        super(ServerUniverse, self).startingSoon(msg)

        # Kick all AI players now, the game is about to begin.
        for p in list(self.players):
            if p.bot:
                self.game.sendServerCommand(RemovePlayerMsg(p.id))

    def checkForResult(self):
        msg = self.state.getFinishedMessage(self)
        if msg is not None:
            self.game.sendServerCommand(msg)

    @TickMsg.handler
    def tickReceived(self, msg):
        super(ServerUniverse, self).tickReceived(msg)

        self.checkForResult()
        self.changeGameStateIfNeeded()
        if self.state == gameStates.Ended:
            self.checkForRabbitsAllDead()

    def changeGameStateIfNeeded(self):
        if ((self.state not in (gameStates.Lobby, gameStates.Ended)) or
                self._onceOnly):
            return
        if self.timer.getElapsedTime() < self._nextGameStateCheck:
            return
        self._nextGameStateCheck = (
            self.timer.getElapsedTime() + GAME_STATE_CHECK_PERIOD)

        if self.state == gameStates.Ended:     # At least one rabbit survived!
            log.debug('Time to return to lobby')
            self.game.sendServerCommand(ReturnToLobbyMsg())
            return
        assert self.state == gameStates.Lobby
        self.startNewGameIfReady()

    def startNewGameIfReady(self):
        if self.layoutDatabase is None:
            return
        self._gameStarter.startNewGameIfReady()

    def setNextGameType(self, gameType):
        '''
        @param gameType: string representing next game type.
        '''
        self.getStartingGameStateFromString(gameType)
        self.nextGameType = gameType

    def getNextGameType(self):
        return self.nextGameType

    def checkForRabbitsAllDead(self):
        log.debug('checking for rabbits all dead')
        if all(p.team is None for p in self.players):
            self.game.sendServerCommand(ReturnToLobbyMsg())

    @TrosballTagMsg.handler
    def handle_TrosballTagMsg(self, msg):
        super(ServerUniverse, self).handle_TrosballTagMsg(msg)
        WeakCallLater(
            4, self, '_startGame', None, (
                self.layout.halfMapWidth,
                self.layout.mapHeight),
            4)

    def setGameState(self, state):
        self._gameStarter = state.getGameStarter(self, self._startGame)
        super(ServerUniverse, self).setGameState(state)

    @WorldResetMsg.handler
    def gotWorldReset(self, msg):
        super(ServerUniverse, self).gotWorldReset(msg)
        self.starSpawner.reset()
        self.onReset()

    @GameStartMsg.handler
    def gameStart(self, msg):
        super(ServerUniverse, self).gameStart(msg)
        self.starSpawner.reset()
