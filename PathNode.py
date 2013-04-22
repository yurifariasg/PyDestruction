import math
import Map

class PathNode(object):

    def __init__(self, rect, isBlocked = False):
        self.adjacentNodes = []
        self.rect = rect
        self.blocked = isBlocked
        self.parent = None # This will only be used on PathFinding Algorithms
    
    def addAdjacentNode(self, node):
        self.adjacentNodes.append(node)
    
    def getAdjacentNodes(self, filterBlocked=True, filterFromBombs=[]):
        filteredAdjacents = []
        for node in self.adjacentNodes:
            if not node.isInRangeOfBombs(filterFromBombs) and not node.isBlocked():
                filteredAdjacents.append(node)
        return filteredAdjacents
    
    def isBlocked(self):
        return self.blocked
    
    def setIsBlocked(self, isBlocked):
        self.blocked = isBlocked
        
    def isInRangeOfBomb(self, bomb):
        mycoords = Map.Map.convertRealCoordinatesToBlockyCoordinates(self.rect.center)
        bombcoords = Map.Map.convertRealCoordinatesToBlockyCoordinates(bomb.rect.center)
        
        if mycoords[0] == bombcoords[0]: # Same Vertical
            if mycoords[0] % 2 == 1:
                return True
        
        if mycoords[1] == bombcoords[1]: # Same Horizontal
            if mycoords[1] % 2 == 1:
                return True
        return False
    
    def isInRangeOfBombs(self, bombs):
        for bomb in bombs:
            if self.isInRangeOfBomb(bomb):
                return True
        return False
    
    
    def getClosestAdjacentNodeFrom(self, pos, filterBlocked=True, filterFromBombs=[]):
        closestDis = 1000
        closestNode = None
        for node in self.adjacentNodes:
            for bomb in filterFromBombs:
                if self.isInRangeOfBomb(bomb):
                    continue
            if PathNode.dist(node.rect.center, pos) < closestDis \
                and (not filterBlocked or not node.isBlocked()):
                closestNode = node
                closestDis = PathNode.dist(node.rect.center, pos)
        if PathNode.dist(pos, self.rect.center) < closestDis:
            return self
        else:
            return closestNode
    
    @classmethod
    def dist(cls, pos1, pos2):
        return math.sqrt(
                         math.pow(pos1[0] - pos2[0], 2) +
                         math.pow(pos1[1] - pos2[1], 2))