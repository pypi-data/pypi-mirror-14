'''upgrades.py - defines the behaviour of upgrades.'''

import logging

import pygame

from trosnoth.model.shot import GrenadeShot

log = logging.getLogger('upgrades')

upgradeOfType = {}
allUpgrades = set()


def registerUpgrade(upgradeClass):
    '''
    Marks the given upgrade class to be used in the game.
    '''
    specialUpgrade(upgradeClass)
    allUpgrades.add(upgradeClass)

    return upgradeClass


def specialUpgrade(upgradeClass):
    '''
    Marks the given upgrade class as a special upgrade that can be used only
    via the console.
    '''
    if upgradeClass.upgradeType in upgradeOfType:
        raise KeyError('2 upgrades with %r' % (upgradeClass.upgradeType,))
    upgradeOfType[upgradeClass.upgradeType] = upgradeClass

    return upgradeClass


class Upgrade(object):
    '''Represents an upgrade that can be bought.'''
    goneWhenDie = True
    defaultKey = None
    iconPath = None
    iconColourKey = None
    enabled = True
    applyLocally = False

    # If this flag is set, instead of waiting for a verdict from the server,
    # the client will guess whether a purchase of this upgrade will be allowed,
    # and go on that assumption until it finds out otherwise. This exists so
    # that grenades can feel responsive even if there's high latency.
    doNotWaitForServer = False

    # Upgrades have an upgradeType: this must be a unique, single-character
    # value.
    def __init__(self, player):
        self.universe = player.world
        self.player = player
        self.verified = False

    def __str__(self):
        return self.name

    def use(self):
        '''Initiate the upgrade (server-side)'''
        pass

    def localUse(self, localState):
        '''Initiate the upgrade (client-side)'''
        if self.applyLocally:
            self.use()

    def serverVerified(self, localState):
        '''
        Called client-side when the server has confirmed that this upgrade is
        allowed. This is most useful as a hook for upgrade classes which set
        the doNotWaitForServer flag.
        '''
        self.verified = True

    def deniedByServer(self, localState):
        '''
        Called client-side when a doNotWaitForServer upgrade needs to be
        canceled because the server did not approve it.
        '''
        self.delete()

    def delete(self):
        '''
        Performs any necessary tasks to remove this upgrade from the game.
        '''
        self.player.upgrade = None

    def timeIsUp(self):
        '''
        Called by the universe when the upgrade's time has run out.
        '''
        pass


@registerUpgrade
class Shield(Upgrade):
    '''
    shield: protects player from one shot
    '''
    upgradeType = 's'
    requiredStars = 4
    timeRemaining = 30
    name = 'Shield'
    action = 'shield'
    order = 20
    defaultKey = pygame.K_2
    iconPath = 'upgrade-shield.png'

    def __init__(self, player):
        super(Shield, self).__init__(player)
        self.maxProtections = self.universe.physics.playerRespawnHealth
        self.protections = self.maxProtections


@specialUpgrade
class PhaseShift(Upgrade):
    '''
    phase shift: affected player cannot be shot, but cannot shoot.
    '''
    upgradeType = 'h'
    requiredStars = 6
    timeRemaining = 25
    name = 'Phase Shift'
    action = 'phase shift'
    order = 40
    defaultKey = pygame.K_4
    iconPath = 'upgrade-phaseshift.png'


@specialUpgrade
class Turret(Upgrade):
    '''
    turret: turns a player into a turret; a more powerful player, although one
    who is unable to move.
    '''
    upgradeType = 't'
    requiredStars = 8
    timeRemaining = 50
    name = 'Turret'
    action = 'turret'
    order = 10
    defaultKey = pygame.K_1
    iconPath = 'upgrade-turret.png'

    def use(self):
        '''Initiate the upgrade'''
        self.player.detachFromEverything()
        self.zone = zone = self.player.getZone()
        if not zone:
            return
        if zone.turretedPlayer is not None:
            zone.turretPlayer.upgrade.delete()
        zone.turretedPlayer = self.player

        # Arrest vertical movement so that upon losing the upgrade, the
        # player doesn't re-jump
        self.player.yVel = 0

    def delete(self):
        '''Performs any necessary tasks to remove this upgrade from the game'''
        self.player.turretOverHeated = False
        self.player.turretHeat = 0.0
        if self.zone:
            self.zone.turretedPlayer = None
        super(Turret, self).delete()


@registerUpgrade
class MinimapDisruption(Upgrade):
    upgradeType = 'm'
    requiredStars = 15
    timeRemaining = 40
    name = 'Minimap Disruption'
    action = 'minimap disruption'
    order = 30
    defaultKey = pygame.K_3
    iconPath = 'upgrade-minimap.png'

    def use(self):
        if self.player.team is not None:
            self.player.team.usingMinimapDisruption = True

    def delete(self):
        if self.player.team is not None:
            self.player.team.usingMinimapDisruption = False
            super(MinimapDisruption, self).delete()


@registerUpgrade
class Grenade(Upgrade):
    upgradeType = 'g'
    requiredStars = 7
    timeRemaining = 2.5
    goneWhenDie = False
    numShots = 40
    name = 'Grenade'
    action = 'grenade'
    order = 50
    defaultKey = pygame.K_5
    iconPath = 'upgrade-grenade.png'
    doNotWaitForServer = True

    def localUse(self, localState):
        localState.grenadeLaunched()

    def serverVerified(self, localState):
        super(Grenade, self).serverVerified(localState)
        localState.matchGrenade()

    def deniedByServer(self, localState):
        super(Grenade, self).deniedByServer(localState)
        localState.grenadeRemoved()

    def use(self):
        '''Initiate the upgrade.'''
        self.player.world.addGrenade(
            GrenadeShot(self.player.world, self.player, self.timeRemaining))


@registerUpgrade
class Ricochet(Upgrade):
    upgradeType = 'r'
    requiredStars = 3
    timeRemaining = 10
    name = 'Ricochet'
    action = 'ricochet'
    order = 60
    defaultKey = pygame.K_6
    iconPath = 'upgrade-ricochet.png'


@registerUpgrade
class Ninja (Upgrade):
    '''allows you to become invisible to all players on the opposing team'''
    upgradeType = 'n'
    requiredStars = 5
    timeRemaining = 25
    name = 'Ninja'
    action = 'phase shift'  # So old phase shift hotkeys trigger ninja.
    order = 40
    defaultKey = pygame.K_4
    iconPath = 'upgrade-ninja.png'
    iconColourKey = (254, 254, 253)


@registerUpgrade
class Shoxwave(Upgrade):
    '''
    shockwave: upgrade that will replace shots with a shockwave like that of
    the grenade vaporising all enemies and enemy shots in the radius of blast.
    '''
    upgradeType = 'w'
    requiredStars = 7
    timeRemaining = 45
    name = 'Shoxwave'
    action = 'shoxwave'
    order = 80
    defaultKey = pygame.K_7
    iconPath = 'upgrade-shoxwave.png'
    iconColourKey = (255, 255, 255)


@registerUpgrade
class MachineGun(Upgrade):
    upgradeType = 'x'
    requiredStars = 10
    timeRemaining = 30
    name = 'Machine Gun'
    action = 'turret'   # So that old turret hotkeys trigger machine gun.
    order = 10
    defaultKey = pygame.K_1
    iconPath = 'upgrade-machinegun.png'
    applyLocally = True

    def use(self):
        self.player.mgBulletsRemaining = 15
        self.player.mgFiring = False

    def delete(self):
        super(MachineGun, self).delete()
        self.player.mgBulletsRemaining = 0


@registerUpgrade
class Bomber(Upgrade):
    upgradeType = 'b'
    requiredStars = 1
    timeRemaining = 6
    name = 'Bomber'
    action = 'bomber'
    order = 90
    defaultKey = pygame.K_8
    iconPath = 'upgrade-bomber.png'

    def timeIsUp(self):
        super(Bomber, self).delete()
        self.universe.bomberExploded(self.player)


@specialUpgrade
class RespawnFreezer(Upgrade):
    '''
    Respawn freezer: upgrade that will render spawn points unusable.
    '''
    upgradeType = 'f'
    requiredStars = 8
    timeRemaining = 30
    name = 'Respawn Freezer'
    action = 'respawn freezer'
    order = 100
    defaultKey = pygame.K_9
    iconPath = 'upgrade-freezer.png'

    def use(self):
        '''Initiate the upgrade'''
        self.zone = self.player.getZone()
        self.zone.frozen = True

    def delete(self):
        '''Performs any necessary tasks to remove this upgrade from the game'''
        super(RespawnFreezer, self).delete()
        if self.zone:
            self.zone.frozen = False


@specialUpgrade
class Directatorship(Upgrade):
    '''
    Directatorship: shielded ninja ricochet machine gunner.
    '''
    upgradeType = 'd'
    requiredStars = 150
    timeRemaining = 60
    name = 'Directatorship'
    action = 'directatorship'
    order = 200
    maxProtections = protections = 5
