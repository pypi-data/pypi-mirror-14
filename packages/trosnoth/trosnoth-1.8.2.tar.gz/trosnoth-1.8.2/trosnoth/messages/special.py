import logging

from trosnoth.messages.base import AgentRequest, ServerCommand

log = logging.getLogger()


class PlayerHasElephantMsg(ServerCommand):
    idString = 'jken'
    fields = 'playerId'
    packspec = 'c'


class PlayerHasTrosballMsg(ServerCommand):
    idString = 'ball'
    fields = 'playerId'
    packspec = 'c'


class TrosballPositionMsg(ServerCommand):
    idString = 'bing'
    fields = 'xpos', 'ypos', 'xvel', 'yvel'
    packspec = 'ffff'


class ThrowTrosballMsg(AgentRequest):
    idString = 'pass'
    fields = 'tickId'
    packspec = 'H'

    def clientValidate(self, localState, world, sendResponse):
        if not localState.player:
            return False
        if localState.player.id != world.trosballPlayer.id:
            return False
        return True

    def serverApply(self, game, agent):
        if agent.player and agent.player == game.world.trosballPlayer:
            game.world.throwTrosball()


class TrosballTagMsg(ServerCommand):
    idString = 'goal'
    fields = 'teamId', 'playerId'
    packspec = 'cc'


class AchievementUnlockedMsg(ServerCommand):
    idString = 'Achm'
    fields = 'playerId', 'achievementId'
    packspec = 'c*'
