from Bomb import *
from Fire import *
from Block import *
from Bomberman import *
import PathNode

class Physics(object):

    def __init__(self, map):
        self.map = map
    
    def update(self): ## EXPERIMENTAL
        # Update Bombs
        b_index = 0
        while b_index < len(self.map.bombs):
            bomb = self.map.bombs[b_index]
            bomb.update()
            if bomb.state == BombState.TIMED_OUT:
                self.map.bombs.pop(b_index)
                self.setBlockFree(bomb.rect.center)
                self.addFire((bomb.rect.x, bomb.rect.y), bomb.range)
            else:
                b_index += 1
        
        # Update Fire
        f_index = 0
        while f_index < len(self.map.fire):
            fire = self.map.fire[f_index]
            fire.update()
            if fire.state == FireState.EXTINGUISHED:
                wall = fire.wall_destroyed
                if wall != None and isinstance(wall, Block) and wall.type == Block.DESTRUCTABLE and wall in self.map.walls:
                    self.map.walls.remove(wall)
                    self.setBlockFree(wall.rect.center)
                    
                self.map.fire.pop(f_index)
            else:
                f_index += 1
        
        for player in self.map.players:
            player.rect.x += player.speed_x
            player.rect.y += player.speed_y
            collided = False
            slide = None
            for wall in self.map.walls:
                if wall.rect.colliderect(player.rect):
                    collided = True
                    
                    # Sliding
                    if player.speed_x > 0:
                        if player.rect.y > wall.rect.y and wall.type == Block.FIXED:
                            slide = Direction.DOWN
                        elif player.rect.y < wall.rect.y and wall.type == Block.FIXED:
                            slide = Direction.UP
                    if player.speed_x < 0:
                        if player.rect.y > wall.rect.y and wall.type == Block.FIXED:
                            slide = Direction.DOWN
                        elif player.rect.y < wall.rect.y and wall.type == Block.FIXED:
                            slide = Direction.UP
                    if player.speed_y > 0:
                        if player.rect.x > wall.rect.x and wall.type == Block.FIXED:
                            slide = Direction.RIGHT
                        elif player.rect.x < wall.rect.x and wall.type == Block.FIXED:
                            slide = Direction.LEFT
                    if player.speed_y < 0:
                        if player.rect.x > wall.rect.x and wall.type == Block.FIXED:
                            slide = Direction.RIGHT
                        elif player.rect.x < wall.rect.x and wall.type == Block.FIXED:
                            slide = Direction.LEFT
                    break # Skip next walls
            
            if not collided: # yet!
                for bomb in self.map.bombs:
                    if bomb.rect.colliderect(player.rect):
                        if not (bomb.state == BombState.PLACING and player in bomb.colliders):
                            collided = True
                            slide = None
                            break
                    elif player in bomb.colliders:
                        bomb.colliders.remove(player)
            
            if collided:
                player.rect.x -= player.speed_x
                player.rect.y -= player.speed_y
                if slide: # Sliding if next block is not blocked
                    playerBlockCoord = self.map.convertRealCoordinatesToBlockyCoordinates(player.rect.center)
                    if slide == Direction.UP and \
                            not self.blockIsBlocked([playerBlockCoord[0], playerBlockCoord[1] - 1]):
                        player.rect.y -= 1
                    elif slide == Direction.DOWN and \
                            not self.blockIsBlocked([playerBlockCoord[0], playerBlockCoord[1] + 1]):
                        player.rect.y += 1
                    elif slide == Direction.LEFT and \
                            not self.blockIsBlocked([playerBlockCoord[0] - 1, playerBlockCoord[1]]):
                        player.rect.x -= 1
                    elif slide == Direction.RIGHT and \
                            not self.blockIsBlocked([playerBlockCoord[0] + 1, playerBlockCoord[1]]):
                        player.rect.x += 1
            
            player.speed_x = 0
            player.speed_y = 0
    
    def setBlockFree(self, worldCoords):
        blockyCoords = self.map.convertRealCoordinatesToBlockyCoordinates(worldCoords)
        self.map.blockyMap[blockyCoords[1]][blockyCoords[0]].setIsBlocked(False)
        
    def blockIsBlocked(self, blockyCoords):
        block = self.map.blockyMap[blockyCoords[1]][blockyCoords[0]]
        if isinstance(block, PathNode.PathNode):
            return block.isBlocked()
        return False
            
    def addFire(self, position, range):
        
        self.map.fire.append(Fire(position, FireType.CENTER))
        self.add_fire_on_direction(position, range, Direction.LEFT)
        self.add_fire_on_direction(position, range, Direction.RIGHT)
        self.add_fire_on_direction(position, range, Direction.UP)
        self.add_fire_on_direction(position, range, Direction.DOWN)
        
            
    def add_fire_on_direction(self, center, range, direction):
        
        currentPos = list(center)
        # Set up depending on Direction
        if direction == Direction.RIGHT:
            currentPos[0] += Settings.BLOCK_SIZE
            max_position_range = [center[0] + (Settings.BLOCK_SIZE * range), currentPos[1]]
            last_fire_position = [max_position_range[0] - Settings.BLOCK_SIZE, currentPos[1]]
        elif direction == Direction.LEFT:
            currentPos[0] -= Settings.BLOCK_SIZE
            max_position_range = [center[0] + (-1 * Settings.BLOCK_SIZE * range), currentPos[1]]
            last_fire_position = [max_position_range[0] + Settings.BLOCK_SIZE, currentPos[1]]
        elif direction == Direction.UP:
            currentPos[1] -= Settings.BLOCK_SIZE
            max_position_range = [currentPos[0], center[1] + (-1 * Settings.BLOCK_SIZE * range)]
            last_fire_position = [currentPos[0], max_position_range[1] + Settings.BLOCK_SIZE]
        elif direction == Direction.DOWN:
            currentPos[1] += Settings.BLOCK_SIZE
            max_position_range = [currentPos[0], center[1] + (Settings.BLOCK_SIZE * range)]
            last_fire_position = [currentPos[0], max_position_range[1] - Settings.BLOCK_SIZE]
        
        collided = False
        while currentPos != max_position_range and not collided:
            collided_object = self.perform_fire_collision(currentPos)
            collided = collided_object != None
            if currentPos == last_fire_position or \
                        (collided and isinstance(collided_object, Block) and \
                         collided_object.type == Block.DESTRUCTABLE): # Last Fire
                
                # Add Based on Direction
                if direction == Direction.RIGHT:
                    self.map.fire.append(Fire(currentPos, FireType.HORIZONTAL_RIGHT_EDGE, collided_object))
                elif direction == Direction.LEFT:
                    self.map.fire.append(Fire(currentPos, FireType.HORIZONTAL_LEFT_EDGE, collided_object))
                elif direction == Direction.UP:
                    self.map.fire.append(Fire(currentPos, FireType.VERTICAL_TOP_EDGE, collided_object))
                elif direction == Direction.DOWN:
                    self.map.fire.append(Fire(currentPos, FireType.VERTICAL_BOTTOM_EDGE, collided_object))
                    
            elif not collided:
                # Add Based on Direction
                if direction == Direction.RIGHT or direction == Direction.LEFT:
                    self.map.fire.append(Fire(currentPos, FireType.HORIZONTAL))
                elif direction == Direction.UP or direction == Direction.DOWN:
                    self.map.fire.append(Fire(currentPos, FireType.VERTICAL))
            
            if direction == Direction.RIGHT:
                currentPos[0] += Settings.BLOCK_SIZE
            elif direction == Direction.LEFT:
                currentPos[0] -= Settings.BLOCK_SIZE
            elif direction == Direction.UP:
                currentPos[1] -= Settings.BLOCK_SIZE
            elif direction == Direction.DOWN:
                currentPos[1] += Settings.BLOCK_SIZE
        
        
    def perform_fire_collision(self, position):
        players = self.map.get_players_at(position)
        for player in players:
            if not player.invulnerable:
                player.take_damage()
                powerup = player.drop_power()
                self.map.powerups.append(powerup)
        
        bomb = self.map.get_bomb_at(position)
        if bomb != None:
            bomb.state = BombState.TIMED_OUT
            return bomb
        
        wall = self.map.get_wall_at(position)
        if wall != None:
            if wall.type == Block.DESTRUCTABLE:
                pass
            return wall
        
            