import logging

import pygame

from trosnoth.const import MAP_TO_SCREEN_SCALE
from trosnoth.gui.framework import framework
from trosnoth.gui.framework.elements import TextElement, PictureElement
from trosnoth.gui.common import (Location, FullScreenAttachedPoint,
        ScaledSize, Area, CanvasX, Screen, RelativePoint)
from trosnoth.gui.framework.unobtrusiveValueGetter import YesNoGetter

from trosnoth.trosnothgui.ingame.messagebank import MessageBank
from trosnoth.trosnothgui.ingame.stars import StarGroup
from trosnoth.trosnothgui.ingame import mainMenu
from trosnoth.trosnothgui.ingame.gamevote import GameVoteMenu, NicknameBox
from trosnoth.trosnothgui.ingame.gauges import (TurretGauge, RespawnGauge,
        UpgradeGauge, GunGauge, StarGauge)
from trosnoth.trosnothgui.ingame.achievementBox import AchievementBox
from trosnoth.trosnothgui.ingame.chatBox import ChatBox
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
from trosnoth.gui.framework.dialogbox import DialogResult
from trosnoth.trosnothgui.settings.settings import SettingsMenu

from trosnoth.model.upgrades import (allUpgrades, Grenade, Ninja, Turret,
        Directatorship, Ricochet, Shoxwave)

from trosnoth.messages import (BuyUpgradeMsg, AbandonUpgradeMsg,
        RespawnRequestMsg, ChangeNicknameMsg, PlayerIsReadyMsg,
        ThrowTrosballMsg)

log = logging.getLogger('detailsInterface')


class DetailsInterface(framework.CompoundElement):
    '''Interface containing all the overlays onto the screen:
    chat messages, player lists, gauges, stars, etc.'''
    def __init__(self, app, gameInterface):
        super(DetailsInterface, self).__init__(app)
        self.gameInterface = gameInterface

        # Maximum number of messages viewable at any one time
        maxView = 8

        self.world = gameInterface.world
        self.player = None
        font = app.screenManager.fonts.messageFont
        self.currentMessages = MessageBank(self.app, maxView, 50,
                Location(FullScreenAttachedPoint(ScaledSize(-40,-40),
                'bottomright'), 'bottomright'), 'right', 'bottom', font)

        # If we want to keep a record of all messages and their senders
        self.input = None
        self.inputText = None
        self.unobtrusiveGetter = None
        self.turretGauge = None
        self.reloadGauge = GunGauge(self.app, Area(
                FullScreenAttachedPoint(ScaledSize(0,-60), 'midbottom'),
                ScaledSize(100,30), 'midbottom'))
        self.respawnGauge = None
        self.upgradeGauge = None
        self.achievementBox = None
        self.currentUpgrade = None
        self.starGroup = StarGroup(self.app)
        self.settingsMenu = SettingsMenu(app, onClose=self.hideSettings,
                showThemes=False)

        self.chatBox = ChatBox(app, self.world, self.gameInterface)

        menuloc = Location(FullScreenAttachedPoint((0,0), 'bottomleft'),
                'bottomleft')
        self.menuManager = mainMenu.MainMenu(self.app, menuloc, self,
                self.gameInterface.keyMapping)
        self.upgradeDisplay = UpgradeDisplay(app)
        self.trajectoryOverlay = TrajectoryOverlay(app, gameInterface.gameViewer.viewManager, self.upgradeDisplay)
        self.gameVoteMenu = GameVoteMenu(
            app, self.world, onChange=self._castGameVote)
        self._gameVoteUpdateCounter = 0
        self.elements = [
            self.currentMessages, self.upgradeDisplay, self.reloadGauge,
            self.starGroup, self.gameVoteMenu, self.chatBox,
            self.trajectoryOverlay, self.menuManager,
        ]

        self.upgradeMap = dict((upgradeClass.action, upgradeClass) for
                upgradeClass in allUpgrades)

    def sendRequest(self, msg):
        return self.gameInterface.sendRequest(msg)

    def tick(self, deltaT):
        super(DetailsInterface, self).tick(deltaT)
        if self.player is None:
            self.gameVoteMenu.active = False
            return
        else:
            if self._gameVoteUpdateCounter <= 0:
                self.gameVoteMenu.update(self.player)
                self._gameVoteUpdateCounter = 25
            else:
                self._gameVoteUpdateCounter -= 1

        self._updateTurretGauge()
        self._updateRespawnGauge()
        self._updateUpgradeGauge()
        self._updateAchievementBox()
        self._updateGameVoteMenu()

    def _castGameVote(self, msg):
        self.sendRequest(msg)

    def _updateGameVoteMenu(self):
        if self.world.canVote():
            self.gameVoteMenu.active = True
        else:
            self.gameVoteMenu.active = False

    def localAchievement(self, achievementId):
        if self.achievementBox is None:
            self.achievementBox = AchievementBox(self.app, self.player,
                                                 achievementId)
            self.elements.append(self.achievementBox)
        else:
            self.achievementBox.addAchievement(achievementId)

    def _updateAchievementBox(self):
        if (self.achievementBox is not None and
                len(self.achievementBox.achievements) == 0):
            self.elements.remove(self.achievementBox)
            self.achievementBox = None

    def _updateTurretGauge(self):
        player = self.player
        if self.turretGauge is None:
            if player.turret:
                self.turretGauge = TurretGauge(self.app, Area(
                        FullScreenAttachedPoint(ScaledSize(0,-100),
                        'midbottom'), ScaledSize(100,30), 'midbottom'),
                        player)
                self.elements.append(self.turretGauge)
        elif not player.turret:
            self.elements.remove(self.turretGauge)
            self.turretGauge = None

    def _updateRespawnGauge(self):
        player = self.player
        if self.respawnGauge is None:
            if player.dead:
                self.respawnGauge = RespawnGauge(self.app, Area(
                        FullScreenAttachedPoint(ScaledSize(0,-20),
                        'midbottom'), ScaledSize(100,30), 'midbottom'),
                        player, self.world)
                self.elements.append(self.respawnGauge)
        elif not player.dead:
            self.elements.remove(self.respawnGauge)
            self.respawnGauge = None

    def _updateUpgradeGauge(self):
        player = self.player
        if self.upgradeGauge is None:
            if player.upgrade is not None:
                self.upgradeGauge = UpgradeGauge(self.app, Area(
                        FullScreenAttachedPoint(ScaledSize(0,-20),
                        'midbottom'), ScaledSize(100,30), 'midbottom'),
                        player)
                self.elements.append(self.upgradeGauge)
        elif player.upgrade is None:
            self.elements.remove(self.upgradeGauge)
            self.upgradeGauge = None

    def gameOver(self, winningTeam):
        self.gameInterface.gameOver(winningTeam)

    def setPlayer(self, player):
        self.player = player
        self.player.onPrivateChatReceived.addListener(self.privateChat)
        self.reloadGauge.player = player

    def showSettings(self):
        if self.settingsMenu not in self.elements:
            self.elements.append(self.settingsMenu)

    def hideSettings(self):
        if self.settingsMenu in self.elements:
            self.elements.remove(self.settingsMenu)
            self.gameInterface.updateKeyMapping()

    def _setCurrentUpgrade(self, upgradeType):
        self.currentUpgrade = upgradeType
        self.upgradeDisplay.setUpgrade(self.currentUpgrade, self.player)
        self.menuManager.manager.reset()

    def _requestUpgrade(self):
        if self.player.hasTrosball():
            self.sendRequest(ThrowTrosballMsg(self.getTickId()))
        elif self.currentUpgrade is not None:
            self.sendRequest(BuyUpgradeMsg(
                self.currentUpgrade.upgradeType, self.getTickId()))

    def _changeNickname(self):
        if not self.world.canRename():
            self.newMessage('Cannot change nickname after game has started',
                    self.app.theme.colours.errorMessageColour)
            return

        prompt = NicknameBox(self.app)
        @prompt.onClose.addListener
        def _customEntered():
            if prompt.result == DialogResult.OK:
                nickname = prompt.value
                self.sendRequest(ChangeNicknameMsg(self.player.id,
                        nickname.encode()))

        prompt.show()

    def getTickId(self):
        return self.world.lastTickId

    def doAction(self, action):
        '''
        Activated by hotkey or menu.
        action corresponds to the action name in the keyMapping.
        '''
        if action == 'leaderboard':
            self.showPlayerDetails()
            self.menuManager.manager.reset()
        elif action == 'toggle interface':
            self.toggleInterface()
            self.menuManager.manager.reset()
        elif action == 'more actions':
            self.menuManager.showMoreMenu()
        elif action == 'settings':
            self.showSettings()
        elif action == 'maybeLeave':
            self.menuManager.showQuitMenu()
        elif action == 'leave':
            # Disconnect from the server.
            self.gameInterface.disconnect()
        elif action == 'join':
            # Join if currently spectating
            self.gameInterface.spectatorWantsToJoin()
        elif action == 'menu':
            # Return to main menu and show or hide the menu.
            self.menuManager.escape()
        elif action == 'toggle terminal':
            self.gameInterface.toggleTerminal()
        elif self.gameInterface.gameViewer.replay:
            # Replay-specific actions
            if action in ('follow', 'activate upgrade'):
                # Follow the game action
                self.gameInterface.gameViewer.setTarget(None)
        else:
            # All actions after this line should require a player.
            if self.player is None:
                return
            if action == 'respawn':
                self.sendRequest(RespawnRequestMsg(tickId=self.getTickId()))
            elif action == 'ready':
                if self.player.readyToStart or self.player.readyForTournament:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, False,
                            False))
                else:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, True,
                            False))
            elif action in self.upgradeMap:
                self._setCurrentUpgrade(self.upgradeMap[action])
            elif action == 'no upgrade':
                self._setCurrentUpgrade(None)
                self.menuManager.manager.reset()
            elif action == 'abandon':
                self.abandon(self.player)
                self.menuManager.manager.reset()
            elif action == 'chat':
                self.chat()
                self.menuManager.manager.reset()
            elif action == 'select upgrade':
                self.menuManager.showBuyMenu()
            elif action == 'activate upgrade':
                self._requestUpgrade()
            elif action == 'change nickname':
                self._changeNickname()
            elif action not in ('jump', 'right', 'left', 'down'):
                log.warning('Unknown action: %r', action)

    def newMessage(self, text, colour=None, error=False):
        if colour is None:
            if error:
                colour = self.app.theme.colours.errorMessageColour
            else:
                colour = self.app.theme.colours.grey
        self.currentMessages.newMessage(text, colour)

    def privateChat(self, text, sender):
        # Destined for the one player
        text = " (private): " + text
        self.newChat(text, sender)

    def newChat(self, text, sender):
        if sender is None:
            self.chatBox.newServerMessage(text)
        else:
            colour = self.app.theme.colours.chatColour(sender.team)
            self.chatBox.newMessage(text, sender.nick, colour)

    def endInput(self):
        if self.input:
            self.elements.remove(self.input)
            self.input = None
        if self.inputText:
            self.elements.remove(self.inputText)
            self.inputText = None
        if self.unobtrusiveGetter:
            self.elements.remove(self.unobtrusiveGetter)
            self.unobtrusiveGetter = None
        if self.menuManager not in self.elements:
            self.elements.append(self.menuManager)
        self.input = self.inputText = None


    def inputStarted(self):
        self.elements.append(self.input)
        self.elements.append(self.inputText)
        self.input.onEsc.addListener(lambda sender: self.endInput())
        self.input.onEnter.addListener(lambda sender: self.endInput())

        try:
            self.elements.remove(self.menuManager)
        except ValueError:
            pass

    def chat(self):
        if not self.player:
            return

        if self.chatBox.isOpen():
            self.chatBox.close()
        else:
            pygame.key.set_repeat(300, 30)
            self.chatBox.open()
            self.chatBox.setPlayer(self.player)

    def abandon(self, player):
        '''
        Called when a player says they wish to abandon their upgrade.
        '''
        if player.upgrade:
            addOn = 'upgrade'
            if type(player.upgrade) == Grenade:
                self.newMessage('Cannot abandon an active grenade!',
                        self.app.theme.colours.errorMessageColour)
                return
        else:
            return

        message = 'Really abandon your ' + addOn + ' (Y/N)'
        self.endInput()
        self.unobtrusiveGetter = YesNoGetter(self.app, Location(
                FullScreenAttachedPoint((0,0), 'center'), 'center'), message,
                self.app.screenManager.fonts.unobtrusivePromptFont,
                self.app.theme.colours.unobtrusivePromptColour, 3)
        self.elements.append(self.unobtrusiveGetter)

        def gotValue(abandon):
            if self.unobtrusiveGetter:
                self.elements.remove(self.unobtrusiveGetter)
                self.unobtrusiveGetter = None
            if abandon:
                self.sendRequest(
                    AbandonUpgradeMsg(player.id, tickId=self.getTickId()))

        self.unobtrusiveGetter.onGotValue.addListener(gotValue)

    def upgradeUsed(self, player):
        upgrade = player.upgrade
        if upgrade is None:
            upgrade = 'an upgrade'
        else:
            upgrade = str(upgrade)

        if type(player.upgrade) == Grenade:
            message = '%s has thrown a %s' % (player.nick, player.upgrade)
        elif type(player.upgrade) in [Ninja, Turret]:
            message = '%s has become a %s' % (player.nick, player.upgrade)
        elif type(player.upgrade) == Directatorship:
            message = '%s has become a Directator' % player.nick
        elif type(player.upgrade) in [Ricochet, Shoxwave]:
            message = '%s is using %s' % (player.nick, player.upgrade)
        else:
            message = '%s is using a %s' % (player.nick, player.upgrade)

        self.newMessage(message)

    def showPlayerDetails(self):
        self.gameInterface.gameViewer.toggleLeaderBoard()

    def toggleInterface(self):
        self.gameInterface.gameViewer.toggleInterface()

class UpgradeDisplay(framework.CompoundElement):

    def __init__(self, app):
        super(UpgradeDisplay, self).__init__(app)
        self.player = None
        self.upgrade = None

    def refresh(self):
        self.setUpgrade(self.upgrade, self.player)

    def setUpgrade(self, upgradeType, player):
        self.player = player
        self.upgrade = upgradeType
        if player is None or upgradeType is None:
            self.elements = []
        else:
            pos = Location(Screen(0.6, 0), 'midtop')
            image = self.app.theme.sprites.upgradeImage(upgradeType)
            area = Area(
                RelativePoint(Screen(0.6, 0), (0, 52)),
                ScaledSize(50, 10), 'midtop')
            self.elements = [
                PictureElement(self.app, image, pos),
            ]

            if upgradeType.enabled:
                self.elements.append(
                    StarGauge(self.app, area, player, upgradeType))
            else:
                self.elements.append(
                    TextElement(self.app, 'DISABLED',
                        self.app.screenManager.fonts.ingameMenuFont,
                        Location(CanvasX(620, 68), 'midbottom'),
                        self.app.theme.colours.errorMessageColour))

class TrajectoryOverlay(framework.Element):
    def __init__(self, app, viewManager, upgradeDisplay):
        super(TrajectoryOverlay, self).__init__(app)
        self.viewManager = viewManager
        self.upgradeDisplay = upgradeDisplay
        self.enabled = False

    def setEnabled(self, enable):
        self.enabled = enable

    def isActive(self):
        if not self.enabled:
            return False

        player = self.viewManager.getTargetPlayer()

        if not player.hasTrosball() and (self.upgradeDisplay.upgrade is None or self.upgradeDisplay.upgrade.name != 'Grenade' or player.getTeamStars() < Grenade.requiredStars):
            # Nothing to throw yet
            return False

        if player is None:
            return False

        trajectory = player.currentProjectileTrajectory
        if trajectory is None:
            return False
        return True

    def draw(self, surface):
        if not self.isActive():
            return

        player = self.viewManager.getTargetPlayer()
        trajectory = player.currentProjectileTrajectory

        focus = self.viewManager._focus
        area = self.viewManager.sRect

        points = list(trajectory.predictedTrajectoryPoints())
        numPoints = len(points)
        greenToYellow = [(i, 255, 0) for i in range(0, 255, 255 / (numPoints / 2 + numPoints % 2))]
        yellowToRed = [(255, i, 0) for i in range(255, 0, -255 / (numPoints / 2))]

        colours = [(0, 255, 0)] + greenToYellow + yellowToRed

        lastPoint = None
        for item in zip(points, colours):
            point = item[0]
            colour = item[1]
            # Set first point
            if lastPoint is None:
                lastPoint = point
                adjustedPoint = mapPosToScreen(point, focus, area)
                pygame.draw.circle(surface, colour, adjustedPoint, 2)
                continue


            adjustedPoint = mapPosToScreen(point, focus, area)
            adjustedLastPoint = mapPosToScreen(lastPoint, focus, area)

            pygame.draw.line(surface, colour, adjustedLastPoint, adjustedPoint, 5)

            lastPoint = point

        pygame.draw.circle(surface, colour, adjustedPoint, 2)

        radius = int(trajectory.explosionRadius() * MAP_TO_SCREEN_SCALE)
        if radius > 0:
            pygame.draw.circle(surface, (0,0,0), adjustedPoint, radius, 2)
