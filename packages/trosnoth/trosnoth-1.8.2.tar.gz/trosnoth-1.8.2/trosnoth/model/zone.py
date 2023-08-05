import random
import logging
import string

from trosnoth.utils import math

log = logging.getLogger('zone')


class ZoneDef(object):
    '''Stores static information about the zone.

    Attributes:
        adjacentZones - mapping from adjacent ZoneDef objects to collection of
            map blocks joining the zones.
        id - the zone id
        initialOwner - the team that initially owned this zone,
            represented as a number (0 for neutral, 1 or 2 for a team).
        pos - the coordinates of this zone in the map
    '''

    def __init__(self, id, initialOwnerIndex, xCoord, yCoord):
        self.adjacentZones = {}
        self.id = id
        self.initialOwnerIndex = initialOwnerIndex
        self.pos = xCoord, yCoord
        self.bodyBlocks = []
        self.interfaceBlocks = []

        primes, index = divmod(id, 26)
        self.label = string.uppercase[index] + "'" * primes

    ##
    # Return a tuple of adjacent zones, and whether each connection is open
    def zones_AdjInfo(self):
        ret = []
        for adj, blocks in self.adjacentZones.iteritems():
            ret.append((adj, not blocks[0].blocked))
        return tuple(ret)

    def __str__(self):
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id

    def randomPosition(self):
        '''
        Returns a random position in this zone.
        '''
        if random.random() * 3 > 1:
            return random.choice(self.bodyBlocks).randomPosition()
        return random.choice(self.interfaceBlocks).randomPositionInZone(self)


class ZoneState(object):
    '''Represents information about a given zone and its state.

    Attributes:
        universe
        dark - boolean
        owner - a team
        players - a Group
        turretedPlayer - None or a Player

    Attributes which should (eventually) be completely migrated to the zoneDef:
        id
    '''

    def __init__(self, universe, zoneDef):
        self.defn = zoneDef
        self.id = zoneDef.id

        universe.zoneWithDef[zoneDef] = self

        self.universe = universe
        teamIndex = zoneDef.initialOwnerIndex
        if teamIndex is None:
            self.owner = None
            self.dark = False
        else:
            self.owner = universe.teams[teamIndex]
            self.dark = True

            # Tell the team object that it owns one more zone
            self.owner.zoneGained()

        self.previousOwner = self.owner

        self.players = set()
        self.turretedPlayer = None
        self.frozen = False

    def __str__(self):
        # Debug: uniquely identify this zone within the universe.
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id

    def isNeutral(self):
        return self.owner is None

    def tag(self, player):
        '''This method should be called when the orb in this zone is tagged'''
        self.previousOwner = self.owner
        self.dark = False

        # Inform the team objects
        if self.owner:
            self.owner.zoneLost()
        if player is not None:
            team = player.team
            if team is not None:
                team.zoneGained()
            player.incrementStars()
        else:
            team = None

        self.owner = team
        for zone in self.getAdjacentZones():
            if zone.owner == team or self.isNeutral():
                # Allow the adjacent zone to check if it is entirely
                # surrounded by non-enemy zones
                zone.makeDarkIfNeeded()
        self.makeDarkIfNeeded()

    def updateByTrosballPosition(self, position):
        self.isDark = False
        if abs(position[0] - self.defn.pos[0]) < 1e-5:
            self.owner = None
        elif position[0] < self.defn.pos[0]:
            self.owner = self.universe.teams[1]
        else:
            self.owner = self.universe.teams[0]

    def isEnemyTeam(self, team):
        return team != self.owner and team is not None

    def setOwnership(self, team, dark):
        if self.owner is not None:
            self.owner.zoneLost()
        self.owner = team
        if team is not None:
            team.zoneGained()
        self.dark = dark

    def isDark(self):
        return self.dark

    def makeDarkIfNeeded(self):
        '''This method should be called by an adjacent friendly zone that has
        been tagged and gained. It will check to see if it now has all
        surrounding orbs owned by the same team, in which case it will
        change its zone ownership.'''

        # If the zone is already owned, ignore it
        if not self.dark and self.owner is not None:
            for zone in self.getAdjacentZones():
                if self.isEnemyTeam(zone.owner):
                    break
            else:
                self.dark = True

    def playerIsWithinTaggingDistance(self, player):
        tagDistance = 35
        distance = math.distance(self.defn.pos, player.pos)
        return distance < tagDistance

    def getContiguousZones(self):
        '''
        Returns a set of all contiguous zones with orb owned by the same team
        as this zone.
        '''
        owner = self.owner
        sector = set()
        stack = [self]
        while stack:
            zone = stack.pop()
            if zone in sector:
                continue
            sector.add(zone)
            for adjacentZone in zone.getAdjacentZones():
                if adjacentZone.owner == owner:
                    stack.append(adjacentZone)
        return sector

    def playerWhoTaggedThisZone(self):
        '''
        Checks to see whether the zone has been tagged. If not, return None.
        If it has, return a tuple of the player and team who tagged it.
        If the zone has been rendered Neutral, this will be None, None
        '''
        teamsToPlayers = self.getCountedPlayersByTeam()
        teamsWhoCanTag = self.teamsAbleToTag()
        taggingPlayers = []

        if (len(teamsWhoCanTag) == 1 and list(teamsWhoCanTag)[0] ==
                self.owner):
            # No need to check again - we are already the owner
            return

        for team in teamsWhoCanTag:
            for player in teamsToPlayers[team]:
                if self.playerIsWithinTaggingDistance(player):
                    taggingPlayers.append(player)
                    # Only allow one player from each team to have tagged it.
                    break
        if len(taggingPlayers) == 2:
            # Both teams tagged - becomes neutral
            return (None, None)
        elif (len(taggingPlayers) == 1 and list(taggingPlayers)[0].team !=
                self.owner):
            return (taggingPlayers[0], taggingPlayers[0].team)
        else:
            return None

    def clearPlayers(self):
        self.players.clear()

    def addPlayer(self, player):
        '''Adds a player to this zone'''
        self.players.add(player)

    def getCountedPlayersByTeam(self):
        result = dict((team, []) for team in self.universe.teams)

        for player in self.players:
            if player.dead or player.turret:
                # Turreted players do not count as a player for the purpose
                # of reckoning whether an enemy can capture the orb
                continue
            if player.team is not None:
                result[player.team].append(player)
        return result

    def getPlayerCounts(self):
        '''
        Returns a list of (count, teams) ordered by count descending, where
        count is the number of counted (living non-turret) players in the zone
        and teams is the teams with that number of players. Excludes teams
        which do not own the zone and cannot capture it.
        '''
        teamsByCount = {}
        for team, players in self.getCountedPlayersByTeam().iteritems():
            if (
                    team != self.owner
                    and not self.adjacentToAnotherZoneOwnedBy(team)):
                # If the enemy team doesn't have an adjacent zone, they don't
                # count towards numerical advantage.
                continue
            teamsByCount.setdefault(len(players), []).append(team)

        return sorted(teamsByCount.iteritems(), reverse=True)

    def isCapturableBy(self, team):
        '''
        Returns True or False depending on whether this zone can be captured by
        the given team. This takes into account both the zone location and the
        number of players in the zone.
        '''
        return team != self.owner and team in self.teamsAbleToTag()

    def isDisputed(self):
        '''
        Returns a value indicating whether this is a disputed zone. A disputed
        zone is defined as a zone which cannot be tagged by any enemy team, but
        could be if there was one more enemy player in the zone.
        '''
        moreThanThreeDefenders = False

        playerCounts = self.getPlayerCounts()
        while playerCounts:
            count, teams = playerCounts.pop(0)
            if moreThanThreeDefenders and count < 3:
                return False

            if count == 0:
                if any(t != self.owner for t in teams):
                    # There is a team which could tag if it had one attacker
                    return True

            elif count < 3:
                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not disputed.
                    return False

                # If an attacking team had one more player they could capture
                return True

            elif count == 3:
                if moreThanThreeDefenders:
                    return True

                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not disputed.
                    return False

                # Team could capture if it had 4 attackers
                return True

            else:
                if any(t != self.owner for t in teams):
                    # Already capturable
                    return False

                moreThanThreeDefenders = True

        return False

    def getAdjacentZones(self):
        '''
        Iterates through ZoneStates adjacent to this one.
        '''
        for adjZoneDef in self.defn.adjacentZones:
            yield self.universe.zoneWithDef[adjZoneDef]

    def getUnblockedNeighbours(self):
        '''
        Iterates through ZoneStates adjacent to this one which are not blocked
        off.
        '''
        for adjZoneDef, blocks in self.defn.adjacentZones.iteritems():
            if not blocks[0].blocked:
                yield self.universe.zoneWithDef[adjZoneDef]

    def adjacentToAnotherZoneOwnedBy(self, team):
        '''
        Returns whether or not this zone is adjacent to a zone whose orb is
        owned by the given team.
        '''
        for adjZone in self.getAdjacentZones():
            if adjZone.owner == team:
                return True
        return False

    def teamsAbleToTag(self):
        '''
        Returns the set of teams who have enough players to tag a zone
        (ignoring current zone ownership). Teams must have:
         (a) strict numerical advantage in this zone; or
         (b) more than 3 players in this zone.
        This takes into account the fact that turrets do not count towards
        numerical advantage.
        '''
        result = set()

        playerCounts = self.getPlayerCounts()
        while playerCounts:
            count, teams = playerCounts.pop(0)
            if count <= 3:
                if not result and len(teams) == 1 and count > 0:
                    result.update(teams)
                break
            result.update(teams)
        return result

    @staticmethod
    def canTag(numTaggers, numDefenders):
        '''
        Deprecated, do not use.
        '''
        return numTaggers > numDefenders or numTaggers > 3

    def consequenceOfCapture(self):
        '''
        Uses the zone neutralisation logic to calculate how many zone points an
        enemy team would gain by capturing this zone. That is, 2 points for the
        zone itself, plus one for each zone neutralised in the process.
        '''
        if self.owner is None:
            # Always one point for capturing a neutral zone
            return 1

        seen = {self}
        explore = [z for z in self.getAdjacentZones() if z.owner == self.owner]
        sectors = []
        while explore:
            zone = explore.pop(0)
            if zone in seen:
                continue

            thisSector = [zone]
            score = 0
            while thisSector:
                score += 1
                zone = thisSector.pop(0)
                seen.add(zone)
                for z in zone.getAdjacentZones():
                    if z.owner == self.owner and z not in seen:
                        thisSector.append(z)
            sectors.append(score)

        if sectors:
            # Largest sector is not lost
            sectors.remove(max(sectors))

        # Two points for capture, plus one for each zone neutralised
        return 2 + sum(sectors)
