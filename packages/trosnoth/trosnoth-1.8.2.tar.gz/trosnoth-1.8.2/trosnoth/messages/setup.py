import logging

from trosnoth.const import (
    GAME_FULL_REASON, UNAUTHORISED_REASON, NICK_USED_REASON, BAD_NICK_REASON,
    USER_IN_GAME_REASON, ALREADY_JOINED_REASON,
)
from trosnoth.messages.base import (
    AgentRequest, ServerCommand, ServerResponse, ClientCommand,
)
from trosnoth.messages.special import PlayerHasElephantMsg
from trosnoth.model.universe_base import NeutralTeamId
from trosnoth.utils.netmsg import NetworkMessage

log = logging.getLogger(__name__)


####################
# Setup
####################

class InitClientMsg(NetworkMessage):
    idString = 'wlcm'
    fields = 'settings'
    packspec = '*'


class ConnectionLostMsg(ServerCommand):
    # Doesn't really originate on the server.
    fields = ()
    isControl = True
    packspec = ''

    def applyOrderToWorld(self, world):
        pass


class WorldResetMsg(ServerCommand):
    idString = 'rset'
    fields = 'settings'
    packspec = '*'


class ZoneStateMsg(ServerCommand):
    idString = 'ZnSt'
    fields = 'zoneId', 'teamId', 'dark'
    packspec = 'Icb'


class WorldLoadingMsg(ServerCommand):
    idString = 'wait'
    fields = 'loading'
    packspec = 'b'

    def applyOrderToWorld(self, world):
        world.loading = self.loading


####################
# Game
####################

class ChangeNicknameMsg(ClientCommand):
    idString = 'Nick'
    fields = 'playerId', 'nickname'
    packspec = 'c*'

    def serverApply(self, game, agent):
        if game.world.gameIsInProgress():
            return
        p = game.world.getPlayer(self.playerId)
        if not p:
            return

        nick = self.nickname.decode()
        if not game.world.isValidNick(nick):
            return

        for player in game.world.players:
            if p != player and player.nick.lower() == nick.lower():
                # Nick in use.
                return

        if game.world.authManager is not None:
            if game.world.authManager.checkUsername(nick) and (
                    p.user is None or nick.lower() != p.user.username):
                # Nick is someone else's username.
                return

        game.sendServerCommand(self)
        if p.user:
            p.user.setNick(nick)

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        if player:
            player.nick = self.nickname.decode()

    def applyOrderToLocalState(self, localState, world):
        player = localState.player
        if player and player.id == self.playerId:
            player.nick = self.nickname.decode()


class PlayerIsReadyMsg(ClientCommand):
    idString = 'Redy'
    fields = 'playerId', 'ready', 'tournament'
    packspec = 'c??'

    def serverApply(self, game, agent):
        game.sendServerCommand(self)

    def applyOrderToWorld(self, world):
        self.applyToPlayer(world.getPlayer(self.playerId))

    def applyOrderToLocalState(self, localState, world):
        player = localState.player
        if player and player.id == self.playerId:
            self.applyToPlayer(player)

    def applyToPlayer(self, player):
        player.readyToStart = self.ready
        player.readyForTournament = (
            self.tournament and player.prefersTournamentTeam)


class SetPreferredTeamMsg(AgentRequest):
    idString = 'TmNm'
    fields = 'name'
    packspec = '*'

    MAX_TEAM_NAME_LENGTH = 30

    def serverApply(self, game, agent):
        if agent.player is None:
            return
        teamName = self.name.decode()[:self.MAX_TEAM_NAME_LENGTH]
        game.sendServerCommand(PreferredTeamSelectedMsg(
            agent.player.id,
            game.world.isTournamentTeam(teamName),
            teamName.encode()))


class PreferredTeamSelectedMsg(ServerCommand):
    idString = 'TmNm'
    fields = 'playerId', 'tournament', 'name'
    packspec = 'c?*'

    def applyOrderToWorld(self, world):
        self.applyToPlayer(world.getPlayer(self.playerId))

    def applyOrderToLocalState(self, localState, world):
        player = localState.player
        if player and player.id == self.playerId:
            self.applyToPlayer(player)

    def applyToPlayer(self, player):
        player.preferredTeam = self.name.decode()
        player.prefersTournamentTeam = self.tournament
        if not player.prefersTournamentTeam:
            player.readyForTournament = False


class SetPreferredSizeMsg(ClientCommand):
    idString = 'Size'
    fields = 'playerId', 'halfMapWidth', 'mapHeight'
    packspec = 'cBB'

    MAX_MAP_HEIGHT = 10
    MAX_HALF_WIDTH = 10

    def serverApply(self, game, agent):
        if game.world.getPlayer(self.playerId):
            halfMapWidth = min(self.halfMapWidth, self.MAX_HALF_WIDTH)
            mapHeight = min(self.mapHeight, self.MAX_MAP_HEIGHT)
            game.sendServerCommand(
                SetPreferredSizeMsg(self.playerId, halfMapWidth, mapHeight))

    def applyOrderToWorld(self, world):
        self.applyToPlayer(world.getPlayer(self.playerId))

    def applyOrderToLocalState(self, localState, world):
        player = localState.player
        if player and player.id == self.playerId:
            self.applyToPlayer(player)

    def applyToPlayer(self, player):
        player.preferredSize = (self.halfMapWidth, self.mapHeight)


class SetPreferredDurationMsg(ClientCommand):
    '''
    duration is in seconds.
    '''
    idString = 'Dr8n'
    fields = 'playerId', 'duration'
    packspec = 'cI'

    MAX_GAME_DURATION = 86400

    def serverApply(self, game, agent):
        if game.world.getPlayer(self.playerId):
            duration = min(self.duration, self.MAX_GAME_DURATION)
            game.sendServerCommand(
                SetPreferredDurationMsg(self.playerId, duration))

    def applyOrderToWorld(self, world):
        self.applyToPlayer(world.getPlayer(self.playerId))

    def applyOrderToLocalState(self, localState, world):
        player = localState.player
        if player and player.id == self.playerId:
            self.applyToPlayer(player)

    def applyToPlayer(self, player):
        player.preferredDuration = self.duration


class GameStartMsg(ServerCommand):
    idString = 'Go!!'
    fields = ()
    packspec = ''


class GameOverMsg(ServerCommand):
    idString = 'Stop'
    fields = 'teamId', 'timeOver'
    packspec = 'cB'


class ReturnToLobbyMsg(ServerCommand):
    idString = 'Loby'
    fields = ()
    packspec = ''


class SetGameModeMsg(ServerCommand):
    idString = 'Mode'
    fields = 'gameMode'
    packspec = '*'

    def applyOrderToWorld(self, world):
        world.setGameMode(self.gameMode.decode())


class SetGameSpeedMsg(ServerCommand):
    idString = 'Spee'
    fields = 'gameSpeed'
    packspec = 'f'

    def applyOrderToWorld(self, world):
        world.setGameSpeed(self.gameSpeed)


class SetTeamNameMsg(ServerCommand):
    idString = 'Team'
    fields = 'teamId', 'name'
    packspec = 'c*'

    def applyOrderToWorld(self, world):
        if self.teamId == '\x00':
            world.rogueTeamName = self.name
        else:
            team = world.getTeam(self.teamId)
            team.teamName = self.name


class StartingSoonMsg(ServerCommand):
    idString = 'Wait'
    fields = ('delay', 'gameType')
    packspec = 'd*'


class ChangeTimeLimitMsg(ServerCommand):
    idString = 'Time'
    fields = 'timeLimit'
    packspec = 'd'


####################
# Players
####################

class AddPlayerMsg(ServerCommand):
    idString = 'NewP'
    fields = 'playerId', 'teamId', 'zoneId', 'dead', 'bot', 'nick'
    packspec = 'ccIbb*'


class SetPlayerTeamMsg(ServerCommand):
    idString = 'PlTm'
    fields = 'playerId', 'teamId'
    packspec = 'cc'

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        player.team = world.getTeam(self.teamId)

    def applyOrderToLocalState(self, localState, world):
        if localState.player and localState.player.id == self.playerId:
            localState.player.team = world.getTeam(self.teamId)


class RemovePlayerMsg(ServerCommand):
    idString = 'DelP'
    fields = 'playerId'
    packspec = 'c'

    def applyOrderToWorld(self, world):
        world.delPlayer(world.getPlayer(self.playerId))


class JoinRequestMsg(AgentRequest):
    idString = 'Join'
    fields = 'teamId', 'authTag', 'bot', 'nick'
    packspec = 'cQb*'
    authTag = 0
    localBotRequest = False     # Intentionally not sent over wire.

    def serverApply(self, game, agent):
        preferredTeamId = self.teamId
        nick = self.nick.decode()
        teamPlayerCounts = game.world.getTeamPlayerCounts()

        if agent.player is not None:
            agent.messageToAgent(CannotJoinMsg(ALREADY_JOINED_REASON))
            return

        if len(game.world.players) >= game.maxTotalPlayers:
            agent.messageToAgent(CannotJoinMsg(GAME_FULL_REASON))
            return

        teamId = game.world.getTeamToJoin(preferredTeamId)
        if (teamId != NeutralTeamId and teamPlayerCounts.get(teamId, 0) >=
                game.maxPerTeam):
            agent.messageToAgent(CannotJoinMsg(GAME_FULL_REASON))
            return

        if not game.world.isValidNick(nick):
            agent.messageToAgent(CannotJoinMsg(BAD_NICK_REASON))
            return

        preferredTeam = ''
        if game.authTagManager is not None and not self.localBotRequest:
            user = game.authTagManager.checkAuthTag(self.authTag)
            if user is None:
                agent.messageToAgent(CannotJoinMsg(UNAUTHORISED_REASON))
                return
            else:
                for player in game.world.players:
                    if player.user == user:
                        agent.messageToAgent(
                            CannotJoinMsg(USER_IN_GAME_REASON))
                        return
                if (nick.lower() != user.username and
                        game.authTagManager.checkUsername(nick)):
                    agent.messageToAgent(CannotJoinMsg(NICK_USED_REASON))
                    return

                preferredTeam = user.getDefaultTeam()
        else:
            user = None

        # Only check for duplicate nick after checking for auth-related errors.
        usedNicks = {player.nick.lower() for player in game.world.players}
        if self.bot:
            if '-' in nick and nick.rsplit('-', 1)[-1].isdigit():
                base, number = nick.rsplit('-', 1)
                number = int(number)
            else:
                base = nick
                number = 0

            if 'Bot' not in base:
                base += 'Bot'

            while nick.lower() in usedNicks:
                number += 1
                nick = '{}-{}'.format(base, number)
        else:
            if nick.lower() in usedNicks:
                agent.messageToAgent(CannotJoinMsg(NICK_USED_REASON))
                return

        if game.authTagManager is not None and not self.localBotRequest:
            game.authTagManager.discardAuthTag(self.authTag)
            user.setNick(nick)

        playerId = game.idManager.newPlayerId()
        if playerId is None:
            agent.messageToAgent(CannotJoinMsg(GAME_FULL_REASON))
            return

        zoneId = game.world.selectZoneForTeam(teamId).id
        game.sendServerCommand(AddPlayerMsg(
            playerId, teamId, zoneId, True, self.bot, nick.encode()))
        player = game.world.getPlayer(playerId)
        if user:
            player.setUser(user)
        if player.isElephantOwner():
            game.world.sendServerCommand(PlayerHasElephantMsg(playerId))
        game.joinSuccessful(agent, playerId)

        if preferredTeam:
            tournament = game.world.isTournamentTeam(preferredTeam)
            game.sendServerCommand(PreferredTeamSelectedMsg(
                playerId, tournament, preferredTeam.encode()))


class CannotJoinMsg(ServerResponse):
    '''
    Valid reasonId options are defined in trosnoth.const.
    '''
    idString = 'NotP'
    fields = 'reasonId'
    packspec = 'c'


class SetAgentPlayerMsg(ServerCommand):
    '''
    Send back to the agent which requested to join if the join has succeeded.

    This is not a control message, because we only want the successful join to
    be delivered after the player has been added to the universe.
    '''
    idString = 'OwnP'
    fields = 'playerId'
    packspec = 'c'

    def applyOrderToLocalState(self, localState, world):
        localState.agent.setPlayer(world.getPlayer(self.playerId))
