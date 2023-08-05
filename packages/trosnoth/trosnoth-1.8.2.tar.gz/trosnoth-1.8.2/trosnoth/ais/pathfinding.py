import copy
import cPickle
import heapq
import logging
from math import pi
import os
import weakref
import zipfile

from twisted.internet import defer, reactor, threads

from trosnoth import data
from trosnoth.model.mapLayout import LayoutDatabase
from trosnoth.model.player import Player
from trosnoth.model.universe import Universe

log = logging.getLogger(__name__)


DB_FILENAME = data.getPath(data, 'pathfinding.db')

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'
ORB = 'o'

OPPOSITE_DIRECTION = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

ADJACENT_KINDS = {
    'topBlocked': {
        NORTH: [],
        SOUTH: ['btmBlocked', 'btmOpen'],
        EAST: ['bck'],
        WEST: ['fwd'],
    },
    'topOpen': {
        NORTH: ['btmBlocked', 'btmOpen'],
        SOUTH: ['btmBlocked', 'btmOpen'],
        EAST: ['bck'],
        WEST: ['fwd'],
    },
    'btmBlocked': {
        NORTH: ['topBlocked', 'topOpen'],
        SOUTH: [],
        EAST: ['fwd'],
        WEST: ['bck'],
    },
    'btmOpen': {
        NORTH: ['topBlocked', 'topOpen'],
        SOUTH: ['topBlocked', 'topOpen'],
        EAST: ['fwd'],
        WEST: ['bck'],
    },
    'fwd': {
        NORTH: ['bck'],
        SOUTH: ['bck'],
        EAST: ['topBlocked', 'topOpen'],
        WEST: ['btmBlocked', 'btmOpen'],
    },
    'bck': {
        NORTH: ['fwd'],
        SOUTH: ['fwd'],
        EAST: ['btmBlocked', 'btmOpen'],
        WEST: ['topBlocked', 'topOpen'],
    },
}


class ActionKindCollection(object):
    def __init__(self):
        self.store = {}

    def register(self, cls):
        key = cls.__name__
        if key in self.store:
            raise KeyError('Another %s already registered', key)
        self.store[key] = cls
        return cls

    def getByString(self, key):
        return self.store[key]

    def actionKindToString(self, actionKind):
        key = actionKind.__name__
        assert self.store[key] == actionKind
        return key

actionKindClasses = ActionKindCollection()


class PathFindingAction(object):
    '''
    Represents a possible action for player path-finding.
    '''

    def prepNextStep(self, player):
        '''
        Returns (done, stateChangesfaceRight) where done is a boolean
        indicating whether or not this action is complete, stateChanges is a
        list of (key, value) pairs indicating necessary changes to the player's
        getState() dict, and faceRight is whether or not the player should be
        facing right for this step.
        '''
        raise NotImplementedError(
            '%s.prepNextStep()' % (self.__class__.__name__,))

    @classmethod
    def buildStateChanges(cls, player, desiredState):
        result = []
        for k, v in player._state.iteritems():
            desired = desiredState.get(k, False)
            if v != desired:
                result.append((k, desired))
        return result


class SingleAction(PathFindingAction):

    def __init__(self):
        self.first = True

    @classmethod
    def simulate(cls, player, alsoAllowBlockDefs=()):
        '''
        Applies this action type to the given player object until it is
        complete or it leaves the current map block.
        '''
        action = cls()

        orbTagCost = None

        startMapBlock = player.getMapBlock()
        cost = 0
        while True:
            done, stateChanges, faceRight = action.prepNextStep(player)
            if done:
                break
            for key, value in stateChanges:
                player.updateState(key, value)
            if faceRight and not player.isFacingRight():
                player.lookAt(pi / 2)
            elif (not faceRight) and player.isFacingRight():
                player.lookAt(-pi / 2)
            cost += 1

            player.advance()
            zone = player.getZone()
            if (
                    orbTagCost is None and zone
                    and zone.playerIsWithinTaggingDistance(player)):
                orbTagCost = cost
            playerBlock = player.getMapBlock()
            if playerBlock != startMapBlock:
                if playerBlock.defn not in alsoAllowBlockDefs:
                    break

            if cost >= 300:
                log.warning(
                    'Action %s looks like it will go forever' % (cls,))
                return None, None

        return cost, orbTagCost


@actionKindClasses.register
class FallDown(SingleAction):
    def prepNextStep(self, player):
        stateChanges = self.buildStateChanges(player, {})
        done = not self.first and (
            player.isOnGround() or player.isAttachedToWall())
        self.first = False
        return done, stateChanges, player.isFacingRight()


@actionKindClasses.register
class FallLeft(SingleAction):
    def prepNextStep(self, player):
        stateChanges = self.buildStateChanges(player, {'left': True})
        done = not self.first and (
            player.isOnGround() or player.isAttachedToWall())
        self.first = False
        return done, stateChanges, False


@actionKindClasses.register
class FallRight(SingleAction):
    def prepNextStep(self, player):
        stateChanges = self.buildStateChanges(player, {'right': True})
        done = not self.first and (
            player.isOnGround() or player.isAttachedToWall())
        self.first = False
        return done, stateChanges, True


@actionKindClasses.register
class Drop(SingleAction):
    def prepNextStep(self, player):
        stateChanges = self.buildStateChanges(player, {'down': True})
        done = not self.first
        self.first = False
        return done, stateChanges, player.isFacingRight()


@actionKindClasses.register
class JumpUp(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {}) + [
                ('jump', True)]
            done = False
        elif player._jumpTime > 0:
            stateChanges = self.buildStateChanges(player, {'jump': True})
            done = False
        else:
            stateChanges = self.buildStateChanges(player, {})
            done = player.yVel >= 0
        self.first = False
        return done, stateChanges, player.isFacingRight()


@actionKindClasses.register
class JumpLeft(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'left': True}) + [
                ('jump', True)]
            done = False
        elif player._jumpTime > 0:
            stateChanges = self.buildStateChanges(
                player, {'left': True, 'jump': True})
            done = False
        else:
            stateChanges = self.buildStateChanges(player, {'left': True})
            done = player.yVel >= 0
        self.first = False
        return done, stateChanges, False


@actionKindClasses.register
class JumpRight(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'right': True}) + [
                ('jump', True)]
            done = False
        elif player._jumpTime > 0:
            stateChanges = self.buildStateChanges(
                player, {'right': True, 'jump': True})
            done = False
        else:
            stateChanges = self.buildStateChanges(player, {'right': True})
            done = player.yVel >= 0
        self.first = False
        return done, stateChanges, True


@actionKindClasses.register
class MoveLeft(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'left': True})
            done = False
        else:
            stateChanges = []
            done = True
        self.first = False
        return done, stateChanges, False


@actionKindClasses.register
class MoveRight(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'right': True})
            done = False
        else:
            stateChanges = []
            done = True
        self.first = False
        return done, stateChanges, True


@actionKindClasses.register
class SlowStepLeft(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'left': True})
            done = False
        else:
            stateChanges = []
            done = True
        self.first = False
        return done, stateChanges, True


@actionKindClasses.register
class SlowStepRight(SingleAction):
    def prepNextStep(self, player):
        if self.first:
            stateChanges = self.buildStateChanges(player, {'right': True})
            done = False
        else:
            stateChanges = []
            done = True
        self.first = False
        return done, stateChanges, False


class MultiActionPath(PathFindingAction):
    def __init__(self, actions):
        super(MultiActionPath, self).__init__()
        self.actions = [a() for a in actions]

    def prepNextStep(self, player):
        if not self.actions:
            return True, [], player.isFacingRight()
        while self.actions:
            done, stateChanges, faceRight = self.actions[0].prepNextStep(
                player)
            if done:
                self.actions.pop(0)
            else:
                break
        return (len(self.actions) == 0), stateChanges, faceRight


class RouteToOrb(PathFindingAction):
    def __init__(self, pathFinder, zone):
        super(RouteToOrb, self).__init__()
        self.pathFinder = pathFinder
        self.zone = zone
        self.currentActions = []
        self.steps = None  # Not yet calculated

    def prepNextStep(self, player):
        if self.steps is None:
            if not player.attachedObstacle:
                # Just fall. When we land we can work out what to do.
                return False, [], player.isFacingRight()
            self.calculatePath(player)

        while True:
            if not self.steps:
                # Finished
                return True, [], player.isFacingRight()

            blockDef, scoreKey = self.steps[0]
            if (
                    scoreKey == ORB and
                    player.getZone().playerIsWithinTaggingDistance(player)):
                self.steps = []
                return True, [], player.isFacingRight()

            while self.currentActions:
                done, changes, faceRight = self.currentActions[0].prepNextStep(
                    player)
                if done:
                    self.currentActions.pop(0)
                else:
                    return False, changes, faceRight

            playerMapBlock = player.getMapBlock()
            if playerMapBlock.defn != blockDef:
                self.steps.pop(0)
                if self.steps and playerMapBlock.defn != self.steps[0][0]:
                    log.warning('Ended up in wrong map block!')
                    self.steps = []
                if not self.steps:
                    return True, [], False
                blockDef, scoreKey = self.steps[0]

            blockPaths = self.pathFinder.blocks[blockDef]
            self.currentActions = [
                a() for a in blockPaths.getActions(player, scoreKey)]

            if not self.currentActions:
                # Error case, act like we're done.
                self.steps = []

    def calculatePath(self, player):
        '''
        Use Dijkstra's algorithm to calculate the shortest path through the map
        blocks based on the approximate traversal costs of the map blocks.
        '''
        self.steps = []

        block = player.getMapBlock()
        blockPaths = self.pathFinder.blocks[block.defn]
        playerNode = blockPaths.getNode(player)
        if player.getZone() == self.zone and ORB in playerNode['scores']:
            self.steps.append((block.defn, ORB))
            return

        targets = {}
        for direction in [NORTH, SOUTH, EAST, WEST]:
            if direction in playerNode['scores']:
                targets[blockPaths.getMapBlockNode(direction)] = (
                    playerNode['scores'][direction])

        heap = []
        seen = set()
        finished = object()

        for node in self.pathFinder.getOrbNodes(self.zone):
            heapq.heappush(heap, (0, None, node))

        while heap:
            cost, path, node = heapq.heappop(heap)
            if node in seen:
                continue
            seen.add(node)
            if node is finished:
                break
            if node in targets:
                stepCost = targets[node]
                heapq.heappush(heap, (cost + stepCost, (node, path), finished))
                continue

            for child, stepCost in node.getIncomingPaths():
                heapq.heappush(heap, (cost + stepCost, (node, path), child))

        else:
            # No path found!
            log.warning('No path to orb could be found!')
            return

        while path is not None:
            node, path = path
            self.steps.append((node.blockDef, node.scoreKey))


class PathFindingStore(object):
    def __init__(self):
        self.blocks = {}
        self.combos = {}

    def build(self):
        log.info('Finding allowed nodes and edges...')

        layoutDb = LayoutDatabase()
        ds = layoutDb.datastores[0]
        for (kind, blocked), layouts in ds.layouts.iteritems():
            for layout in layouts:
                log.info('%s', os.path.basename(layout.filename))
                self.addBlock(layout, kind, blocked, layoutDb=layoutDb)

        log.info('Calculating walk scores within blocks...')
        for blockPaths in self.blocks.itervalues():
            blockPaths.calculateDefaultWalkScores()

        log.info('Calculating walk scores between blocks...')
        self.buildBlockCombinations(layoutDb=layoutDb)

        self.save()

    def addBlock(self, blockLayout, kind, blocked, layoutDb=None):
        '''
        Adds the given map block layout to the store and performs the initial
        pass of calculations.
        '''
        if blockLayout.key in self.blocks:
            raise KeyError('%s already in store' % (blockLayout.filename,))
        paths = PreCalculatedMapBlockPaths(blockLayout, kind, blocked)
        self.blocks[blockLayout.key] = paths
        paths.initialiseNodesAndEdges(layoutDb)

    def buildBlockCombinations(self, layoutDb=None):
        '''
        Goes through combinations of blocks which can fit together and
        calculates the costs of walking between the blocks.
        '''
        byKind = {}
        for blockPaths in self.blocks.itervalues():
            key = blockPaths.getKindKey()
            byKind.setdefault(key, []).append(blockPaths)

        for startKind, blockPaths in byKind.iteritems():
            for startBlockPaths in blockPaths:
                for direction, allowedKinds in (
                        ADJACENT_KINDS[startKind].iteritems()):
                    for endKind in allowedKinds:
                        for endBlockPaths in byKind.get(endKind, []):
                            self.addCombo(
                                startBlockPaths, endBlockPaths, direction,
                                layoutDb=layoutDb)

    def addCombo(
            self, startBlockPaths, endBlockPaths, direction, layoutDb=None):
        combo = PreCalculatedMapBlockCombination(
            startBlockPaths, endBlockPaths, direction)
        key = startBlockPaths.layout.key, endBlockPaths.layout.key, direction
        self.combos[key] = combo
        combo.calculateConnections(layoutDb)
        combo.calculateWalkScores()

    def save(self):
        with zipfile.ZipFile(DB_FILENAME, 'w') as z:
            for block in self.blocks.itervalues():
                block.save(z)
            for combo in self.combos.itervalues():
                combo.save(z)


class RunTimePathFinder(object):

    def __init__(self, mapLayout):
        self.layout = mapLayout
        self.blocks = {}

    @defer.inlineCallbacks
    def loadData(self):
        '''
        This method loads from the path finding database, and yields every so
        often so that it can be used to load progressively. This is
        deliberately NOT @inlineCallbacks, in order that the caller can have
        more fine control of how often it loads the next step.
        '''
        blockCache = {}
        comboCache = {}

        with zipfile.ZipFile(DB_FILENAME, 'r') as z:
            for row in self.layout.blocks:
                for blockDef in row:
                    if blockDef.layout is None:
                        continue
                    runTimePaths = yield (
                        PreCalculatedMapBlockPaths.applyToBlock(
                            blockDef, z, blockCache))
                    if runTimePaths:
                        self.blocks[blockDef] = runTimePaths

                    d = defer.Deferred()
                    reactor.callLater(0, d.callback, None)
                    yield d

            for j, row1 in enumerate(self.layout.blocks[:-1]):
                row2 = self.layout.blocks[j + 1]
                for i, blockDef1 in enumerate(row1):
                    blockDef2 = row2[i]
                    if blockDef1.layout is None or blockDef2.layout is None:
                        continue
                    if blockDef1.blocked:
                        continue
                    yield self.blocks[blockDef1].updateForCombination(
                        SOUTH, self.blocks[blockDef2], z, comboCache)
                    yield self.blocks[blockDef2].updateForCombination(
                        NORTH, self.blocks[blockDef1], z, comboCache)

                    d = defer.Deferred()
                    reactor.callLater(0, d.callback, None)
                    yield d

            for row in self.layout.blocks:
                for i, blockDef1 in enumerate(row[:-1]):
                    blockDef2 = row[i + 1]
                    if blockDef1.layout is None or blockDef2.layout is None:
                        continue
                    yield self.blocks[blockDef1].updateForCombination(
                        EAST, self.blocks[blockDef2], z, comboCache)
                    yield self.blocks[blockDef2].updateForCombination(
                        WEST, self.blocks[blockDef1], z, comboCache)

                    d = defer.Deferred()
                    reactor.callLater(0, d.callback, None)
                    yield d

    def getOrbAction(self, player):
        block = player.getMapBlock()
        if block.defn not in self.blocks:
            return None
        return MultiActionPath(self.blocks[block.defn].getActions(player, ORB))

    def getExitAction(self, player, direction):
        block = player.getMapBlock()
        if block.defn not in self.blocks:
            return None
        return MultiActionPath(
            self.blocks[block.defn].getActions(player, direction))

    def getAllActions(self, player):
        block = player.getMapBlock()
        if block.defn not in self.blocks:
            return None
        return self.blocks[block.defn].getAllActions(player)

    def getRouteToOrb(self, zone):
        return RouteToOrb(self, zone)

    def getOrbNodes(self, zone):
        x, y = zone.defn.pos
        j, i = self.layout.getMapBlockIndices(x, y - 5)
        blockDef1 = self.layout.blocks[j][i]
        blockDef2 = self.layout.blocks[j + 1][i]
        yield self.blocks[blockDef1].getMapBlockNode(ORB)
        yield self.blocks[blockDef2].getMapBlockNode(ORB)


class PreCalculatedMapBlockPaths(object):
    def __init__(self, blockLayout, kind, blocked):
        self.kind = kind
        self.blocked = blocked
        self.layout = blockLayout
        self.nodes = {}
        self.outbound = {
            NORTH: PreCalculatedNode(self),
            SOUTH: PreCalculatedNode(self),
            EAST: PreCalculatedNode(self),
            WEST: PreCalculatedNode(self),
        }
        self.orbEdges = set()

    def save(self, z):
        arcName = 'blocks/' + '/'.join(str(i) for i in self.layout.key)
        contents = cPickle.dumps({
            'nodes': [node.serialise() for node in self.nodes.itervalues()],
        }, protocol=cPickle.HIGHEST_PROTOCOL)
        z.writestr(arcName, contents, zipfile.ZIP_DEFLATED)

    @staticmethod
    @defer.inlineCallbacks
    def applyToBlock(blockDef, z, blockCache):
        arcName = 'blocks/' + '/'.join(str(i) for i in blockDef.layout.key)
        if arcName not in blockCache:
            yield threads.deferToThread(
                PreCalculatedMapBlockPaths._loadPathData,
                blockDef, z, arcName, blockCache)

        data = blockCache[arcName]
        defer.returnValue(RunTimeMapBlockPaths(blockDef, data))

    @staticmethod
    def _loadPathData(blockDef, z, arcName, blockCache):
        try:
            f = z.open(arcName)
        except KeyError:
            log.warning(
                'No path finding data found for %s',
                os.path.basename(blockDef.layout.filename)
                + (' (reverse)' if blockDef.layout.reversed else ''),
            )
            blockCache[arcName] = None
            return

        with f:
            blockCache[arcName] = cPickle.load(f)

    def getWorldAndBlockDef(self, layoutDb=None):
        '''
        Creates and returns a dummy world and the block definition
        corresponding to this map block.
        '''
        if layoutDb is None:
            layoutDb = LayoutDatabase()

        world = Universe(layoutDb, 1, 1)

        if self.layout.kind in ('fwd', 'bck'):
            i, j = 2, 1
        elif self.layout.kind == 'top':
            i, j = 1, 1
        else:
            i, j = 1, 2

        block = world.map.layout.blocks[j][i]
        self.layout.applyTo(block)

        return world, block

    def initialiseNodesAndEdges(self, layoutDb=None):
        world, block = self.getWorldAndBlockDef(layoutDb)

        for obstacle in block.obstacles + block.ledges:
            if not obstacle.jumpable:
                continue
            minI, maxI = obstacle.getPositionIndexBounds(Player)
            for i in xrange(minI, maxI + 1):
                node = PreCalculatedNode(self, block, obstacle, i)
                self.nodes[node.obstacleId, i] = node

        for node in self.nodes.itervalues():
            node.expandEdges(world, block)

        log.info(
            '  -> Nodes: %r  Edges: %r  Exits: %r  Orb caps: %r',
            len(self.nodes),
            sum(len(n.outbound) for n in self.nodes.itervalues()),
            sum(len(n.inbound) for n in self.outbound.itervalues()),
            len(self.orbEdges),
        )

    def nodeFromPlayerState(self, player):
        '''
        Finds and returns the node that the given player state is associated
        with.
        '''
        assert player.attachedObstacle.jumpable
        obstacleId = player.attachedObstacle.obstacleId
        posIndex = player.attachedObstacle.getPositionIndex(Player, player.pos)
        return self.nodes[obstacleId, posIndex]

    def getExitNode(self, startBlock, endBlock):
        x0, y0 = startBlock.pos
        x1, y1 = endBlock.pos
        if x1 == x0 and y1 < y0:
            return self.outbound[NORTH]
        if x1 == x0 and y1 > y0:
            return self.outbound[SOUTH]
        if x1 > x0 and y1 == y0:
            return self.outbound[EAST]
        if x1 < x0 and y1 == y0:
            return self.outbound[WEST]
        return None

    def calculateDefaultWalkScores(self):
        '''
        Calculates the minimum distance from each node to any possible way of
        exiting the zone in each direction.
        '''
        for d in [NORTH, SOUTH, EAST, WEST]:
            self.calculateWalkScores(self.outbound[d].inbound, d)
        self.calculateWalkScores(self.orbEdges, ORB, orbCosts=True)

    def calculateWalkScores(self, targetEdges, scoreKey, orbCosts=False):
        '''
        Uses Dijkstra's algorithm to calculate the minimum distance from each
        node in this block to complete any of the given target edges. Stores
        these minimum values using the given scoreKey. If orbCosts is True,
        uses the orb cost of the given edges rather than the actual cost.
        '''
        heap = []
        for edge in targetEdges:
            if orbCosts:
                cost = edge.orbTagCost
            else:
                cost = edge.cost
            heapq.heappush(heap, (cost, edge.startNode))

        seen = set()
        while heap:
            cost, node = heapq.heappop(heap)
            if node in seen:
                continue
            seen.add(node)
            node.setWalkScore(scoreKey, cost)
            for edge in node.inbound:
                if edge.startNode in seen:
                    continue
                heapq.heappush(heap, (cost + edge.cost, edge.startNode))
        log.info(
            '%s -> %s: Visited %r nodes (/%r)',
            os.path.basename(self.layout.filename), scoreKey,
            len(seen), len(self.nodes))

    def getKindKey(self):
        if self.kind in ('top', 'btm'):
            return '%s%s' % (self.kind, 'Blocked' if self.blocked else 'Open')
        return self.kind


class RunTimeMapBlockPaths(object):
    def __init__(self, blockDef, blockData):
        self.blockDef = blockDef

        # Calling copy.deepcopy() on the whole node data takes a long time, so
        # select the ones we're going to be mutating and copy them only.
        self.nodes = {
            data['key']: {
                'edges': data['edges'],     # does not need copying
                'targets': copy.deepcopy(data['targets']),
                'scores': copy.deepcopy(data['scores']),
            } for data in blockData['nodes']
        }

        self.mapBlockNodes = {
            k: RunTimeMapBlockNode(blockDef, k)
            for k in [NORTH, SOUTH, EAST, WEST, ORB]}

    @defer.inlineCallbacks
    def updateForCombination(self, direction, other, z, cache):
        '''
        Called during loading, to update this block's node data with
        information based on what map blocks are adjacent to this one.
        Directionality: if you travel in direction from self, you will get to
        other.
        '''
        # Load the data for the combination
        data = yield PreCalculatedMapBlockCombination.loadData(
            self.blockDef, other.blockDef, direction, z, cache)

        if data is None:
            return

        for nodeKey, cost in data['scores'].iteritems():
            if cost is None:
                del self.nodes[nodeKey]['scores'][direction]
            else:
                self.nodes[nodeKey]['scores'][direction] = cost

        for edgeData in data['edges']:
            nodeKey = edgeData['source']
            self.nodes[nodeKey]['targets'][direction] = {
                'cost': edgeData['cost'],
                'actions': edgeData['actions'],
            }

        # Link the high-level path-finding nodes
        if not data['transitions']:
            log.error(
                'No transition data for %s -> %s: %s',
                os.path.basename(self.blockDef.layout.filename),
                direction,
                os.path.basename(other.blockDef.layout.filename))
        for outDir, cost in data['transitions'].iteritems():
            other.mapBlockNodes[outDir].addInwardEdge(
                self.mapBlockNodes[direction], cost)

    def getNode(self, player):
        obstacleId = player.attachedObstacle.obstacleId
        posIndex = player.attachedObstacle.getPositionIndex(Player, player.pos)
        return self.nodes[obstacleId, posIndex]

    def getBestEdge(self, node, scoreKey):
        if scoreKey in node['targets']:
            return node['targets'][scoreKey]

        def endNodeScore(edge):
            endNode = self.nodes[edge['target']]
            return endNode['scores'][scoreKey]

        def edgeScore(edge):
            return endNodeScore(edge) + edge['cost']

        edges = [
            e for e in node['edges']
            if scoreKey in self.nodes[e['target']]['scores']]
        if not edges:
            return None

        best = min(edges, key=edgeScore)
        if endNodeScore(best) >= node['scores'].get(scoreKey, 10000):
            # Even the best action does not get us closer (should never happen)
            log.warning('Stuck in local minimum (should be impossible)')
            log.warning('Perhaps pathfinding DB needs regenerating.')
            log.warning(
                '(in %s, going to %r)',
                os.path.basename(self.blockDef.layout.filename),
                scoreKey)
            return None

        return best

    def getActions(self, player, scoreKey):
        if not player.attachedObstacle:
            return [Drop]
        edge = self.getBestEdge(self.getNode(player), scoreKey)
        if edge is None:
            return []
        return [actionKindClasses.getByString(a) for a in edge['actions']]

    def getAllActions(self, player):
        if not player.attachedObstacle:
            return [MultiActionPath([Drop])]
        return [
            MultiActionPath([
                actionKindClasses.getByString(a) for a in edge['actions']])
            for edge in self.getNode(player)['edges']
        ]

    def getMapBlockNode(self, scoreKey):
        return self.mapBlockNodes[scoreKey]


class RunTimeMapBlockNode(object):
    '''
    Used to calculate the fastest path through a map at run-time. Represents
    exiting the given block by following the given score key.
    '''

    def __init__(self, blockDef, entryDirection):
        self.blockDef = blockDef
        self.scoreKey = entryDirection
        self.inwardEdges = []

    def __str__(self):
        return '(%s from %s)' % (self.scoreKey, self.blockDef)

    def __repr__(self):
        return 'RunTimeMapBlockNode(%r, %r)' % (
            self.blockDef, self.entryDirection)

    def addInwardEdge(self, node, cost):
        '''
        Should be called only during setup.
        '''
        ownKey = self.scoreKey
        if ownKey == ORB:
            ownKey = NORTH if self.blockDef.kind == 'btm' else SOUTH
        if node.scoreKey == OPPOSITE_DIRECTION[ownKey]:
            # Don't bother with edges that loop forever
            return
        self.inwardEdges.append((node, cost))

    def getIncomingPaths(self):
        '''
        Yields (node, cost) for each RunTimeMapBlockNode that can traverse to
        this node.
        '''
        return iter(self.inwardEdges)


class PreCalculatedMapBlockCombination(object):
    def __init__(self, start, end, direction):
        self.start = start
        self.end = end
        self.direction = direction
        self.edges = {}     # start -> edge
        self.walkScores = {}
        # Note: transitionCosts is the average cost of transitioning through
        # the *end* block given that you came from this direction.
        self.transitionCosts = {}

    def save(self, z):
        arcName = 'combos/%s/%s/%s' % (
            '/'.join(str(i) for i in self.start.layout.key),
            self.direction,
            '/'.join(str(i) for i in self.end.layout.key))

        contents = cPickle.dumps({
            'scores': {
                node.serialiseKey(): cost
                for node, cost in self.walkScores.iteritems()
            },
            'edges': [
                edge.serialiseTargetEdge(self.direction, includeSource=True)
                for edge in self.edges.itervalues()],
            'transitions': self.transitionCosts,
        }, protocol=cPickle.HIGHEST_PROTOCOL)
        z.writestr(arcName, contents, zipfile.ZIP_DEFLATED)

    @staticmethod
    @defer.inlineCallbacks
    def loadData(blockDef1, blockDef2, direction, z, cache):
        arcName = 'combos/%s/%s/%s' % (
            '/'.join(str(i) for i in blockDef1.layout.key),
            direction,
            '/'.join(str(i) for i in blockDef2.layout.key))

        if arcName not in cache:
            yield threads.deferToThread(
                PreCalculatedMapBlockCombination._loadCombinationData,
                blockDef1, blockDef2, direction, z, arcName, cache)

        defer.returnValue(cache[arcName])

    @staticmethod
    def _loadCombinationData(
            blockDef1, blockDef2, direction, z, arcName, cache):
        try:
            f = z.open(arcName)
        except KeyError:
            log.warning(
                'No path finding data found for %s -> %s: %s',
                os.path.basename(blockDef1.layout.filename)
                + (' (reverse)' if blockDef1.layout.reversed else ''),
                direction,
                os.path.basename(blockDef2.layout.filename)
                + (' (reverse)' if blockDef2.layout.reversed else ''),
            )
            log.warning(arcName)
            cache[arcName] = None
            defer.returnValue(None)

        with f:
            cache[arcName] = cPickle.load(f)

    def getWorldAndBlockDefs(self, layoutDb=None):
        world, startBlockDef = self.start.getWorldAndBlockDef(layoutDb)

        if self.start.layout.kind in ('fwd', 'bck'):
            i, j = 2, 1
        elif self.start.layout.kind == 'top':
            i, j = 1, 1
        else:
            i, j = 1, 2

        if self.direction == NORTH:
            j -= 1
        elif self.direction == SOUTH:
            j += 1
        elif self.direction == EAST:
            i += 1
        else:
            assert self.direction == WEST
            i -= 1

        endBlockDef = world.map.layout.blocks[j][i]
        self.end.layout.applyTo(endBlockDef)

        return world, startBlockDef, endBlockDef

    def calculateConnections(self, layoutDb=None):
        '''
        Calculates all edges leaving the start block and ending up in an
        allowable place in the end block.
        '''
        log.info(
            '%s -> %s: %s',
            os.path.basename(self.start.layout.filename) + (
                ' (reverse)' if self.start.layout.reversed else ''),
            self.direction,
            os.path.basename(self.end.layout.filename) + (
                ' (reverse)' if self.end.layout.reversed else ''),
        )

        world, startBlockDef, endBlockDef = self.getWorldAndBlockDefs(layoutDb)

        partitions = {}
        edges = set()

        for edge in self.start.outbound[self.direction].inbound:
            startPlayer = edge.startNode.makePlayerState(world, startBlockDef)

            options = [(edge.actions, startPlayer)]
            while options:
                steps, player = options.pop(0)
                lastAction = steps[-1]
                cost, orbTagCost = lastAction.simulate(
                    player, alsoAllowBlockDefs={endBlockDef})

                if cost is None:
                    # Never ending
                    continue

                endMapBlock = player.getMapBlock()
                if endMapBlock.defn not in (startBlockDef, endBlockDef):
                    # Left both blocks
                    continue

                if player.motionState == 'fall':
                    for actionClass in [FallDown, FallLeft, FallRight]:
                        options.append((steps + [actionClass], player.clone()))
                    continue

                if endMapBlock.defn == startBlockDef:
                    # Back in the starting block
                    continue

                finalNode = self.end.nodeFromPlayerState(player)
                newEdge = PreCalculatedEdge(
                    edge.startNode, steps, finalNode, edge.cost, orbTagCost)
                # Deliberately do not call newEdge.register() because the edge
                # belongs to this block combination, not just to the starting
                # block.
                edges.add(newEdge)
                directions = frozenset(finalNode.walkScores.iterkeys())
                partitions[directions] = partitions.get(directions, 0) + 1

        total = len(edges)
        self.edges = {}
        if edges:
            allDirections = frozenset(d for p in partitions for d in p)
            while allDirections not in partitions:
                worstPartition = min(partitions, key=partitions.get)
                log.warning(
                    '  WARNING: ignoring %r nodes exiting in %r',
                    partitions[worstPartition],
                    ''.join(sorted(worstPartition)))
                del partitions[worstPartition]
                allDirections = frozenset(d for p in partitions for d in p)

            bestPartition = allDirections

            for e in edges:
                if frozenset(e.endNode.walkScores.iterkeys()) == bestPartition:
                    oldEdge = self.edges.get(e.startNode)
                    if oldEdge is None or oldEdge.cost > e.cost:
                        self.edges[e.startNode] = e

            self.transitionCosts = {}
            for outDir in bestPartition:
                costs = [
                    e.endNode.walkScores[outDir]
                    for e in self.edges.itervalues()]
                self.transitionCosts[outDir] = (sum(costs) + 0.) / len(costs)

        log.info('  links: %r total, %r viable', total, len(edges))

    def calculateWalkScores(self):
        '''
        Calculates the walk scores for exiting the start block and ending up in
        the end block. Only stores values which differ from the default walk
        scores in the start block.
        '''

        heap = []
        for edge in self.edges.itervalues():
            heapq.heappush(heap, (edge.cost, edge.startNode))

        seen = set()
        while heap:
            cost, node = heapq.heappop(heap)
            if node in seen:
                continue
            seen.add(node)
            if cost != node.getWalkScore(self.direction):
                self.walkScores[node] = cost
            for edge in node.inbound:
                if edge.startNode in seen:
                    continue
                heapq.heappush(heap, (cost + edge.cost, edge.startNode))

        for node in self.start.nodes.itervalues():
            if node not in seen and self.direction in node.walkScores:
                self.walkScores[node] = None

        log.info(
            '  updated %r/%r nodes (/%r)', len(self.walkScores), len(seen),
            len(self.start.nodes))


class PreCalculatedNode(object):
    def __init__(self, blockPaths, block=None, obstacle=None, posIndex=None):
        self.blockPaths = blockPaths
        self.posIndex = posIndex

        if obstacle is None:
            self.obstacleId = None
            self.pos = None
        else:
            self.obstacleId = obstacle.obstacleId
            pos = obstacle.getPositionFromIndex(Player, posIndex)
            self.pos = (pos[0] - block.pos[0], pos[1] - block.pos[1])

        self.inbound = set()
        self.outbound = set()
        self.walkScores = {}

    def serialise(self):
        '''
        Returns an object that can be serialised using pickle, which contains
        all information about this node that is relevant at run-time.
        '''
        internalEdges = [
            e.serialise() for e in self.outbound
            if e.endNode.obstacleId is not None]

        targetEdges = {}
        orbEdges = [e for e in self.outbound if e.orbTagCost is not None]
        if orbEdges:
            bestOrbEdge = min(orbEdges, key=lambda e: e.orbTagCost)
            targetEdges[ORB] = bestOrbEdge.serialiseTargetEdge(ORB)

        return {
            'key': self.serialiseKey(),
            'edges': internalEdges,
            'targets': targetEdges,
            'scores': self.walkScores,
        }

    def serialiseKey(self):
        return (self.obstacleId, self.posIndex)

    def expandEdges(self, world, blockDef):
        assert not self.outbound

        obstacle = blockDef.getObstacleById(self.obstacleId)

        motionState = Player.getAttachedMotionState(obstacle)

        if motionState == 'fall':
            actionClasses = [FallDown, FallLeft, FallRight]
        elif motionState == 'leftwall':
            actionClasses = [Drop, JumpUp, JumpRight]
        elif motionState == 'rightwall':
            actionClasses = [Drop, JumpUp, JumpLeft]
        else:
            actionClasses = [
                JumpUp, JumpLeft, JumpRight,
                MoveLeft, MoveRight, SlowStepLeft, SlowStepRight]
            if obstacle.drop:
                actionClasses.append(Drop)

        for actionClass in actionClasses:
            self.expandAction(actionClass, world, blockDef, obstacle)

    def expandAction(self, actionClass, world, blockDef, obstacle):
        startPlayer = self.makePlayerState(world, blockDef, obstacle)
        startMapBlock = startPlayer.getMapBlock()

        options = [([actionClass], startPlayer)]
        while options:
            steps, player = options.pop(0)
            lastAction = steps[-1]
            cost, orbTagCost = lastAction.simulate(player)

            if cost is None:
                # Never ending
                continue

            endMapBlock = player.getMapBlock()
            if endMapBlock != startMapBlock:
                finalNode = self.blockPaths.getExitNode(
                    blockDef, endMapBlock.defn)
                if finalNode is None:
                    # Ended up in a non-adjacent map block
                    continue

            elif player.motionState != 'fall':
                finalNode = self.blockPaths.nodeFromPlayerState(player)
            else:
                for actionClass in [FallDown, FallLeft, FallRight]:
                    options.append((steps + [actionClass], player.clone()))
                continue

            edge = PreCalculatedEdge(self, steps, finalNode, cost, orbTagCost)
            edge.register()

    def makePlayerState(self, world, blockDef, obstacle=None):
        if obstacle is None:
            obstacle = blockDef.getObstacleById(self.obstacleId)

        player = Player(world, 'PathFinding', None, None)
        player.pos = (
            self.pos[0] + blockDef.pos[0], self.pos[1] + blockDef.pos[1])
        player.setAttachedObstacle(obstacle)
        return player

    def setWalkScore(self, scoreKey, cost):
        self.walkScores[scoreKey] = cost

    def getWalkScore(self, scoreKey):
        return self.walkScores[scoreKey]


class PreCalculatedEdge(object):
    def __init__(self, startNode, actions, endNode, cost, orbTagCost):
        self.startNode = startNode
        self.actions = actions
        self.endNode = endNode
        self.cost = cost
        self.orbTagCost = orbTagCost

    def register(self):
        self.startNode.outbound.add(self)
        self.endNode.inbound.add(self)
        if self.orbTagCost is not None:
            self.startNode.blockPaths.orbEdges.add(self)

    def serialise(self):
        return {
            'target': self.endNode.serialiseKey(),
            'cost': self.cost,
            'actions': [
                actionKindClasses.actionKindToString(a) for a in self.actions],
        }

    def serialiseTargetEdge(self, targetKey, includeSource=False):
        result = {
            'cost': self.orbTagCost if targetKey == ORB else self.cost,
            'actions': [
                actionKindClasses.actionKindToString(a) for a in self.actions],
        }
        if includeSource:
            result['source'] = self.startNode.serialiseKey()
        return result


pathFindingDBs = weakref.WeakKeyDictionary()


if __name__ == '__main__':
    from trosnoth.utils.utils import initLogging
    initLogging(debug=True)
    PathFindingStore().build()
