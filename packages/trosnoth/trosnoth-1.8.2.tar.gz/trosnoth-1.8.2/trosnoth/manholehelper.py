import logging
import os

from trosnoth.const import OPEN_CHAT
from trosnoth.data import getPath, user, makeDirs
from trosnoth.messages import (
    SetGameModeMsg, SetGameSpeedMsg, UpgradeApprovedMsg, AbandonUpgradeMsg,
    ChangeTimeLimitMsg, SetTeamNameMsg, UpgradeChangedMsg, TrosballTagMsg,
    ChatMsg, ZoneStateMsg, ReturnToLobbyMsg,
)
from trosnoth.model import modes
from trosnoth.model.player import Player
from trosnoth.model.upgrades import allUpgrades, upgradeOfType

log = logging.getLogger(__name__)


class GameModeHelper(object):
    def __init__(self, manholeHelper):
        self.manholeHelper = manholeHelper

    def __repr__(self):
        return 'GameModeHelper<%s>' % (self.manholeHelper.getGameMode(),)

    def __getattr__(self, name):
        if self.manholeHelper.getWorld().physics.hasMode(name):
            return lambda: self.manholeHelper.setGameMode(name)
        raise AttributeError(name)

    def __dir__(self):
        return self.manholeHelper.listGameModes()


class ManholeHelper(object):
    def __init__(self):
        self.mode = GameModeHelper(self)

    def getGame(self):
        raise NotImplementedError('getGame')

    def getWorld(self):
        return self.getGame().world

    def getBanner(self):
        game = self.getGame()
        if game is None:
            return ['\x1b[33mThe server is currently idle.']

        playerCount = sum(1 for p in self.getWorld().players if not p.bot)
        plural = '' if playerCount == 1 else 's'
        result = [
            '\x1b[32mA game is currently running.',
            '\x1b[102m\x1b[30m %d \x1b[49m\x1b[32m player%s online.' % (
                playerCount, plural),
        ]
        return result

    def getGameMode(self):
        '''
        Returns the current game mode.
        '''
        return self.getWorld().gameMode

    def setGameMode(self, gameMode):
        '''
        Changes the current game mode of the world.

        @returns: True if the specified game mode was valid, False otherwise.
        '''
        if self.getWorld().physics.hasMode(gameMode):
            self.getGame().sendServerCommand(SetGameModeMsg(gameMode.encode()))
            return True
        return False

    def listGameModes(self):
        '''
        Returns a list of valid game modes.
        '''
        return [m[len('setMode'):] for m in dir(modes.PhysicsConstants) if
                m.startswith('setMode') if m != 'setMode']

    def trosball(self):
        '''
        Sets the next game to be a Trosball game.
        '''
        self.setNextGameType('trosball')

    def setNextGameType(self, gameType):
        '''
        @param gameType: a string representing the type of game to start next
                time a game begins. For a normal game, use 'normal'.
        '''
        self.getWorld().setNextGameType(gameType)

    def getNextGameType(self):
        return self.getWorld().getNextGameType()

    def getSpeed(self):
        '''
        Returns the current speed of the world as a float, where 1.0 is
        the normal game speed.
        '''

        return self.getWorld()._gameSpeed

    def setSpeed(self, gameSpeed):
        '''
        Changes the speed of the world, where 1.0 is normal speed.

        @param gameSpeed: A positive number
        '''
        self.getGame().sendServerCommand(SetGameSpeedMsg(gameSpeed))

    def pause(self):
        self.setSpeed(0)

    def resume(self):
        self.setSpeed(1)

    def getPlayer(self, nick):
        if isinstance(nick, Player):
            return nick
        for p in self.getWorld().players:
            if p.user == nick or p.nick == nick:
                return p
        return None

    def kickPlayer(self, nick):
        p = self.getPlayer(nick)
        self.getGame().kickPlayer(p.id)

    def startGame(self):
        self.getWorld()._gameStarter.startNewGame()

    def giveUpgrade(self, player, upgradeCode):
        '''
        Gives an upgrade to a player, which is used immediately.

        @param player: Player, nick or username
        @param upgradeCode: Single character upgrade code
        '''
        player = self.getPlayer(player)
        player.pendingUpgrade = upgradeCode
        player.agent.messageToAgent(UpgradeApprovedMsg(upgradeCode))

    def removeUpgrade(self, player):
        '''
        Removes the specified player's current upgrade.

        @param player: Player, nick or username
        '''
        player = self.getPlayer(player)
        currentUpgrade = player.upgrade
        if currentUpgrade is not None:
            # TODO: this may leave the player out of sync, thinking that it
            # still has the upgrade
            self.getGame().sendServerCommand(
                AbandonUpgradeMsg(player.id, self.getWorld().lastTickId))

    def getTimeRemaining(self):
        '''
        Get the amount of time left on the game clock.
        '''
        return self.getWorld().getTimeLeft()

    def endNow(self):
        self.setTimeRemaining(1)

    def setTimeRemaining(self, time):
        '''
        Sets the remaining game time to the given number of seconds or, if None
        is given, to be unlimited.
        '''
        if time is None or time == 0:
            timeLimit = 0
        else:
            timeLimit = time

        self.getGame().sendServerCommand(ChangeTimeLimitMsg(timeLimit))

    def setPlayerLimits(self, maxPerTeam, maxTotal=0):
        '''
        Changes the player limits in the current game. Note that this does not
        affect players who are already in the game.

        @param maxPerTeam: Maximum number of players per team at once
        @param maxTotal: Maximum number of players in the game at once
        '''
        self.getGame().setPlayerLimits(maxPerTeam, maxTotal=maxTotal)

    def setTeamName(self, teamId, teamName):
        '''
        Changes the name of the specified team.

        @param teamId: The id of the team ('A' or 'B')
        @param teamName: The next team name
        '''
        try:
            team = self.getWorld().teamWithId[teamId]
        except KeyError:
            return
        self.getGame().sendServerCommand(
            SetTeamNameMsg(team.id, teamName.encode()))

    def getTeamNames(self):
        '''
        Returns the name of both teams as a tuple.
        '''
        return (
            self.getWorld().teams[0].teamName,
            self.getWorld().teams[1].teamName,
        )

    def getGameState(self):
        '''
        Returns the current state of the game as a string.

        @returns: The text id of the current game state
        '''
        return self.getGame().getGameState()

    def getWinningTeam(self):
        '''
        Returns the winning team.

        If the game hasn't finished yet, the behaviour is undefined.
        @returns: The ID of the winning team or None if it was a draw
        '''
        if self.getWorld().getWinningTeam() is None:
            return None

        return self.getWorld().getWinningTeam().id

    def getZoneCounts(self):
        '''
        Returns the number of zones owned by each team as a tuple.
        '''
        return (
            self.getWorld().teams[0].numZonesOwned,
            self.getWorld().teams[1].numZonesOwned,
        )

    def getUpgradeCosts(self):
        upgrades = {}

        for key, upgrade in upgradeOfType.iteritems():
            upgrades[key] = upgrade.requiredStars
        return upgrades

    def setUpgradeCosts(self, d):
        if isinstance(d, int):
            d = {k: d for k in upgradeOfType}
        for k, v in d.iteritems():
            self.setUpgradeCost(k, v)

    def getUpgrades(self):
        upgrades = []

        for key, upgrade in upgradeOfType.iteritems():
            newUpgrade = {
                "id": key,
                "name": upgrade.name,
                "starCost": upgrade.requiredStars,
                "timeLimit": upgrade.timeRemaining,
                "order": upgrade.order,
                "icon": "upgrade_blank",
                "special": False
            }

            if upgrade not in allUpgrades:
                newUpgrade["order"] += 1000
                newUpgrade["special"] = True

            if upgrade.iconPath is not None:
                newUpgrade["icon"] = upgrade.iconPath.replace("-", "_")[:-4]

            upgrades.append(newUpgrade)

        upgrades.sort(key=lambda upgrade: upgrade["order"])

        return upgrades

    def setUpgradeCost(self, upgradeId, cost):
        '''
        Changes how many stars are required to purchase a particular upgrade.

        @param upgradeId: The single character ID of the upgrade
        @param cost: The new number of stars required.
        '''
        if cost < 0:
            return

        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == upgradeId:
                upgradeClass.requiredStars = cost
                break
        self.getGame().sendServerCommand(
            UpgradeChangedMsg(upgradeId, 'S', cost))

    def setUpgradeTime(self, upgradeId, time):
        '''
        Changes how long a particular upgrade lasts.

        @param upgradeId: The single character ID of the upgrade
        @param time: The time (in seconds) that the upgrade will last for.
            Setting this to 0 will make the upgrade never naturally run out.
        '''
        if time < 0:
            return

        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == upgradeId:
                upgradeClass.timeRemaining = time
                break
        self.getGame().sendServerCommand(
            UpgradeChangedMsg(upgradeId, 'T', time))

    def fixTrosball(self, force=False):
        '''
        Resets the playing field during a game of Trosball.

        Used primarily to fix a stuck Trosball.
        @param force: If True, bypasses several sanity checks
        '''
        state = self.getWorld().state
        if not force:
            if not state.isTrosball():
                return "A Trosball game isn't running right now."
            if self.getWorld().trosballPlayer is not None:
                return '%s has the Trosball: is it really stuck?' % (
                    self.getWorld().trosballPlayer.nick,)

        self.getGame().sendServerCommand(TrosballTagMsg('\x00', '\x00'))

    def sendServerMessage(self, message):
        '''
        Sends a chat message from the server to all players.

        @param message: The message you want everyone to see.
        '''
        self.getGame().sendServerCommand(ChatMsg(OPEN_CHAT, text=message))

    def newWorld(
            self, halfMapWidth=None, mapHeight=None, gameDuration=None,
            blockRatio=0.5):
        if halfMapWidth is None:
            halfMapWidth = self.getWorld().map.layout.halfMapWidth
        if mapHeight is None:
            mapHeight = self.getWorld().map.layout.mapHeight
        layout = self.layoutDatabase.generateRandomMapLayout(
            halfMapWidth, mapHeight, blockRatio=blockRatio)
        self.getWorld().reset(layout, gameDuration)

    def loadMap(self, filename):
        '''
        Loads a map from the .trosnoth/maps directory.

        @param filename: The filename of the map (with extension)
        '''
        game = self.getGame()
        layout = game.layoutDatabase.loadMapFromFile(filename)
        game.world.loadedMap = layout

        return 'Map loaded; it will appear on the next game start.'

    def saveMap(self, filename, force=False):
        '''
        Saves the current map layout to the .trosnoth/maps directory.

        @param filename: The filename of the map (with extension)
        @param force: Overwrites the file if it already exists
        '''
        mapDir = getPath(user, 'maps')
        makeDirs(mapDir)
        filename = os.path.join(mapDir, filename)
        if os.path.exists(filename) and not force:
            return 'File already exists (use "force" parameter to overwrite)'

        with open(filename, 'w') as f:
            f.write(self.getWorld().layout.toString())
        return 'Map saved to %s' % (filename,)

    def ejectMap(self):
        '''
        Unloads any map that was previously loaded.
        '''
        self.getWorld().loadedMap = None

    def enableUpgrade(self, upgradeId):
        '''
        Turns the ability to buy the specified upgrade on.

        @param upgradeId: The single character ID of the upgrade
        '''
        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == upgradeId:
                upgradeClass.enabled = True
        self.getGame().sendServerCommand(UpgradeChangedMsg(upgradeId, 'E', 1))

    def disableUpgrade(self, upgradeId):
        '''
        Turns the ability to buy the specified upgrade off.

        It can still be given via console and all existing upgrades will remain
        active until they expire normally.
        @param upgradeId: The single character ID of the upgrade
        '''
        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == upgradeId:
                upgradeClass.enabled = False
        self.getGame().sendServerCommand(UpgradeChangedMsg(upgradeId, 'E', 0))

    def enableAllUpgrades(self):
        '''
        See documentation for enableUpgrade.
        '''
        for upgradeClass in allUpgrades:
            self.enableUpgrade(upgradeClass.upgradeType)

    def disableAllUpgrades(self):
        '''
        See documentation for disableUpgrade.
        '''
        for upgradeClass in allUpgrades:
            self.disableUpgrade(upgradeClass.upgradeType)

    def changeZoneOwners(self, state):
        '''
        Changes the owner of every zone on the map.

        @param state: A string representing the new owner of each zone.
        It should have a length equal to the number of zones, and the
        characters should be either a team ID, a dash (make neutral) or a
        question mark (don't alter this zone). Spaces are ignored, so you may
        include them for readability. All other characters are invalid.

        Zone counting starts at the top left, then goes top to bottom and
        left to right (in that order).
        '''
        if len(state) != len(self.getWorld().zoneWithId):
            return "Wrong number of zones (expected %d, got %d)" % \
                (len(self.getWorld().zoneWithId), len(state))

        state = state.replace(" ", "").replace("-", "\x00")

        validChars = "".join(self.getWorld().teamWithId.keys()) + "?"

        if state.strip(validChars):
            return "Invalid character in state string"

        for zone, team in enumerate(state):
            newTeam = team
            dark = True

            if team == "?":
                zoneObj = self.getWorld().zoneWithId[zone]
                newTeam = "\x00" if zoneObj.owner is None else zoneObj.owner.id
                dark = zoneObj.dark

            self.getGame().sendServerCommand(ZoneStateMsg(zone, newTeam, dark))

    def reset(self):
        self.getGame().sendServerCommand(ReturnToLobbyMsg())


class AuthServerManholeHelper(ManholeHelper):
    def __init__(self, authFactory):
        self.authFactory = authFactory
        super(AuthServerManholeHelper, self).__init__()

    def getGame(self):
        games = self.authFactory.servers.values()
        if len(games) == 0:
            log.info('getGame: No games available')
            return None
        return games[0].game


class LocalManholeHelper(ManholeHelper):
    def __init__(self, getGame):
        self.getGame = getGame
        super(LocalManholeHelper, self).__init__()
