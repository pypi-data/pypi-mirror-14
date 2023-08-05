import logging
import random

from trosnoth.const import (
    NOT_ENOUGH_STARS_REASON, HAVE_UPGRADE_REASON, PLAYER_DEAD_REASON,
    GAME_NOT_STARTED_REASON, ALREADY_TURRET_REASON, TOO_CLOSE_TO_EDGE_REASON,
    TOO_CLOSE_TO_ORB_REASON, NOT_IN_DARK_ZONE_REASON, ALREADY_DISRUPTED_REASON,
    INVALID_UPGRADE_REASON, DISABLED_UPGRADE_REASON,
)
from trosnoth.messages.base import (
    AgentRequest, ServerCommand, ServerResponse, ClientCommand,
)

log = logging.getLogger(__name__)


EDGE_TURRET_BOUNDARY = 100
ORB_TURRET_BOUNDARY = 150


class AbandonUpgradeMsg(ClientCommand):
    idString = 'DUpg'
    fields = 'playerId', 'tickId'
    packspec = 'cH'
    timestampedPlayerRequest = True

    def clientValidate(self, localState, world, sendResponse):
        player = localState.player
        if player.upgrade is not None and player.upgrade.upgradeType != 'g':
            return True
        return False

    def applyRequestToLocalState(self, localState):
        localState.player.deleteUpgrade()

    def serverApply(self, game, agent):
        player = game.world.getPlayer(self.playerId)
        if player.upgrade is not None and player.upgrade.upgradeType != 'g':
            game.sendServerCommand(self)

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        player.deleteUpgrade(abandoned=True)


class BuyUpgradeMsg(AgentRequest):
    '''
    Signal from interface that a buy has been requested.

    In order for everything to stay in sync, an upgrade purchase works in 3
    steps.

    1. The client sends BuyUpgradeMsg.
    2. The server checks that the stars are avaliable, and replies with
        UpgradeApprovedMsg.
    3. The client sends PlayerHasUpgradeMsg, which is then broadcast to all
        clients.

    To make launching of grenades more responsive, there is a special flag on
    Upgrade classes called doNotWaitForServer. If this flag is set, the client
    assumes that the purchase is successful unless it hears otherwise, and the
    server broadcasts PlayerHasUpgradeMsg immediately at step 2. Step 3 is not
    performed in this case.
    '''
    idString = 'GetU'
    fields = 'upgradeType', 'tickId'
    packspec = 'cH'
    timestampedPlayerRequest = True

    def clientValidate(self, localState, world, sendResponse):
        upgrade = world.getUpgradeType(self.upgradeType)
        if not upgrade.doNotWaitForServer:
            # Don't bother trying to validate locally, let the server decide.
            return True

        player = localState.player
        denialReason = self.getDenialReason(player, upgrade)
        if denialReason:
            response = CannotBuyUpgradeMsg(denialReason)
            response.local = True
            sendResponse(response)
            return False
        return True

    def applyRequestToLocalState(self, localState):
        upgrade = localState.world.getUpgradeType(self.upgradeType)
        if upgrade.doNotWaitForServer:
            localState.player.upgradeUsed(self.upgradeType, local=localState)

    def serverApply(self, game, agent):
        player = agent.player
        if player is None:
            return

        upgrade = player.world.getUpgradeType(self.upgradeType)
        denialReason = self.getDenialReason(player, upgrade)
        if denialReason:
            agent.messageToAgent(CannotBuyUpgradeMsg(denialReason))
        else:
            self._processUpgradePurchase(game, agent, player, upgrade)

    def getDenialReason(self, player, upgrade):
        from trosnoth.model.upgrades import allUpgrades
        if player.upgrade is not None:
            return HAVE_UPGRADE_REASON
        if player.pendingUpgrade is not None:
            return HAVE_UPGRADE_REASON
        if not player.world.abilities.upgrades:
            return GAME_NOT_STARTED_REASON
        if player.dead:
            return PLAYER_DEAD_REASON

        if upgrade not in allUpgrades:
            return INVALID_UPGRADE_REASON

        if not upgrade.enabled:
            return DISABLED_UPGRADE_REASON

        if player.getTeamStars() < upgrade.requiredStars:
            return NOT_ENOUGH_STARS_REASON

        return self._checkUpgradeConditions(player, upgrade)

    def _checkUpgradeConditions(self, player, upgrade):
        '''
        Checks whether the conditions are satisfied for the given player to be
        able to purchase an upgrade of the given kind. Returns None if no
        condition is violated, otherwise returns a one-byte reason code for why
        the upgrade cannot be purchased.
        '''
        from trosnoth.model.upgrades import Turret, MinimapDisruption

        if upgrade is Turret:
            zone = player.getZone()
            if not zone:
                return NOT_IN_DARK_ZONE_REASON
            if not (player.isFriendsWithTeam(zone.owner) and zone.dark):
                return NOT_IN_DARK_ZONE_REASON
            if zone.turretedPlayer is not None:
                return ALREADY_TURRET_REASON
            if player.getMapBlock().fromEdge(player) < EDGE_TURRET_BOUNDARY:
                return TOO_CLOSE_TO_EDGE_REASON

            distanceFromOrb = player.distanceFromCentre()
            if distanceFromOrb < ORB_TURRET_BOUNDARY:
                return TOO_CLOSE_TO_ORB_REASON
        elif upgrade is MinimapDisruption:
            if player.team is None or player.team.usingMinimapDisruption:
                return ALREADY_DISRUPTED_REASON

        return None

    def _processUpgradePurchase(self, game, agent, player, upgrade):
        '''
        Sends the required sequence of messages to gameRequests to indicate
        that the upgrade has been purchased by the player.
        '''
        remaining = upgrade.requiredStars

        # Take from the purchasing player first.
        fromPurchaser = min(player.stars, remaining)
        game.sendServerCommand(PlayerStarsSpentMsg(player.id, fromPurchaser))
        remaining -= fromPurchaser

        # Now take evenly from other team members.
        if remaining > 0:
            players = []
            totalStars = 0
            for p in game.world.players:
                if p.team == player.team and p.id != player.id and p.stars > 0:
                    players.append(p)
                    totalStars += p.stars
            # Order by descending number of stars
            # Shuffle first to avoid biasing any player with the same number of
            # stars as another
            random.shuffle(players)
            players.sort(cmp=lambda p1, p2: cmp(p1.stars, p2.stars))
            players.reverse()

            for p in players:
                fraction = remaining / (totalStars + 0.)
                toGive = int(round(fraction * p.stars))
                remaining -= toGive
                totalStars -= p.stars
                game.sendServerCommand(PlayerStarsSpentMsg(p.id, toGive))
            # Everything should add up
            assert remaining == 0
            assert totalStars == 0

        if upgrade.doNotWaitForServer:
            game.sendServerCommand(PlayerHasUpgradeMsg(
                upgrade.upgradeType, self.tickId, player.id))
        else:
            player.pendingUpgrade = upgrade.upgradeType
            agent.messageToAgent(UpgradeApprovedMsg(upgrade.upgradeType))
        player.onStarsSpent(upgrade.requiredStars)


class PlayerHasUpgradeMsg(ClientCommand):
    '''
    Sent by the local client when it receives word from the server that an
    upgrade purchase has been approved.
    '''
    idString = 'GotU'
    fields = 'upgradeType', 'tickId', 'playerId'
    packspec = 'cHc'
    playerId = '\x00'
    timestampedPlayerRequest = True

    def applyRequestToLocalState(self, localState):
        localState.player.upgradeUsed(self.upgradeType, local=localState)
        # Guaranteed to be verified if the client is sending this in response
        # to UpgradeApprovedMsg.
        localState.player.upgrade.verified = True

    def serverApply(self, game, agent):
        if agent.player and agent.player.pendingUpgrade == self.upgradeType:
            self.playerId = agent.player.id
            agent.player.pendingUpgrade = None
            game.sendServerCommand(self)

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        player.upgradeUsed(self.upgradeType)

    def applyOrderToLocalState(self, localState, world):
        if localState.player and self.playerId == localState.player.id:
            upgrade = localState.player.upgrade
            if upgrade:
                upgrade.serverVerified(localState)


class PlayerStarsSpentMsg(ServerCommand):
    '''
    This message is necessary, because without it a client can't always tell
    where the PlayerHasUpgradeMsg pulled all its stars from.
    '''
    idString = 'Spnt'
    fields = 'playerId', 'count'
    packspec = 'cI'


class AwardPlayerStarMsg(ServerCommand):
    idString = 'Star'
    fields = 'playerId'
    packspec = 'c'

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        player.incrementStars()


class CannotBuyUpgradeMsg(ServerResponse):
    '''
    Tag is the value sent in BuyUpgradeMsg.
    Valid reasonId values are defined in trosnoth.const.
    '''
    idString = 'NotU'
    fields = 'reasonId'
    packspec = 'c'
    local = False

    def applyOrderToLocalState(self, localState, world):
        if self.local:
            return
        if localState.player:
            upgrade = localState.player.upgrade
            if upgrade and not upgrade.verified:
                upgrade.deniedByServer(localState)


class UpgradeApprovedMsg(ServerResponse):
    '''
    Signals to the player that's trying to buy an upgrade that the purchase has
    been successful, and the player should proceed to send a
    PlayerHasUpgradeMsg to use the upgrade. This back and forth is necessary
    because the using of the upgrade needs to happen based on the location of
    the player on their own client's screen, not based on the server's idea of
    where the client is.
    '''
    idString = 'ByOk'
    fields = 'upgradeType'
    packspec = 'c'


class UpgradeChangedMsg(ServerCommand):
    '''
    A message for the clients that informs them of a change in an upgrade stat.
    statType may be:
        'S' - star cost
        'T' - time limit
        'X' - explosion radius
        'E' - enabled
    '''
    idString = 'UpCh'
    fields = 'upgradeType', 'statType', 'newValue'
    packspec = 'ccf'
