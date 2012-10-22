#import Map

class Physics(object):

    def __init__(self, map):
        self.map = map
    
    def update(self): ## EXPERIMENTAL
        for player in self.map.players:
            player.rect.x += player.speed_x
            player.rect.y += player.speed_y
            colided = False
            for wall in self.map.walls:
                if wall.rect.colliderect(player.rect):
                    
                    
                    colided = True
                    break
            
            if colided:
                player.rect.x -= player.speed_x
                player.rect.y -= player.speed_y
            
            player.speed_x = 0
            player.speed_y = 0
            