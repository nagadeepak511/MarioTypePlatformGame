import pygame
from sys import exit
pygame.init()

screen_size = (800,400)
screen = pygame.display.set_mode(screen_size)
time = pygame.time.Clock()

# class definitions

class Platform:
    def __init__(self, pos, size, velocity=0, color='brown'):
        self.pos = pos
        self.size = size
        self.color = color
        self.velocity = velocity
        self.rectangle = pygame.Rect(pos, size)
    def drawFloor(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)
    def isOnScreen(self):
        return self.rectangle.right>0 or self.rectangle.left<800

class Player:
    def __init__(self, pos, rectangle, isEnemy=False, gravity=0, velocity=0, color='green'):
        self.pos = pos
        self.gravity = gravity
        self.velocity = velocity
        self.color = color
        self.rectangle = rectangle
        self.isEnemy=isEnemy
        self.impPlatforms = []
    def drawPlayer(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)

# function definitions

def minDistX(r1, r2):
    d00 = abs(r1.left - r2.left)
    d01 = abs(r1.left - r2.right)
    d02 = abs(r1.right - r2.right)
    d03 = abs(r1.right - r2.left)

    return min(d00, d01, d02, d03)

def minDistY(r1, r2):
    d10 = abs(r1.top - r2.top)
    d11 = abs(r1.top - r2.bottom)
    d12 = abs(r1.bottom - r2.bottom)
    d13 = abs(r1.bottom - r2.top)

    return min(d10, d11, d12, d13)

def minDistBtwnCorners(r1, r2):
    d1 = minDist([r1.rectangle.left, r1.rectangle.top],r2.rectangle)
    d2 = minDist([r1.rectangle.right, r1.rectangle.top],r2.rectangle)
    d3 = minDist([r1.rectangle.right, r1.rectangle.bottom],r2.rectangle)
    d4 = minDist([r1.rectangle.left, r1.rectangle.bottom],r2.rectangle)

    return min(d1, d2, d3, d4)

def TouchingCondition(r1, r2):
    pass

# variables
player = pygame.Rect((250,0),(30,50))

# image loading
player_image = pygame.image.load('Idle (1).png')
left_facing = pygame.image.load('Idle Left (1).png')
jumping_right = pygame.image.load('Jump (4).png')
jumping_left = pygame.image.load('Jump left (4).png')

# text
font = pygame.font.Font(None, 50)
text_surface = font.render("Game over.. press space to reset", "LCD Light.ttf", "red")

player = player_image.get_rect()
player.top = 100
player.left = 250

mainPlayer = Player((250,300),player)
E1 = Player((600,0),pygame.Rect((800-90, 300-50-25),(20,20)), True)
E1.velocity = -2

players = [mainPlayer, E1, Player((50,300-40), pygame.Rect((50,300-40),(20,20)), True)]
players[-1].velocity = 2

platforms = []
platforms += [Platform((0,300),(800, 100))]
platforms += [Platform((200,200-20), (100,20))]
platforms += [Platform((200-100-30,200-40), (100,20))]
platforms += [Platform((200+100+30,200-40), (100,20))]
platforms += [Platform((870,300),(800, 100))]
platforms += [Platform((355,300-18),(100,18))]
platforms += [Platform((0,300-18),(100,18))]
platforms += [Platform((800-90, 300-50), (100,50))]
platforms += [Platform((0,0), (800,100))]

# left right top bottom

run = True
reset = False

while True:
    if reset:
        player = player_image.get_rect()
        player.top = 100
        player.left = 250

        mainPlayer = Player((250,100),player)
        E1 = Player((600,0),pygame.Rect((800-90, 300-50-25),(20,20)), True)
        E1.velocity = -2

        players = [mainPlayer, E1, Player((50,300-40), pygame.Rect((50,300-40),(20,20)), True)]
        players[-1].velocity = 2

        platforms = []
        platforms += [Platform((0,300),(800, 100))]
        platforms += [Platform((200,200-20), (100,20))]
        platforms += [Platform((200-100-30,200-40), (100,20))]
        platforms += [Platform((200+100+30,200-40), (100,20))]
        platforms += [Platform((870,300),(800, 100))]
        platforms += [Platform((355,300-18),(100,18))]
        platforms += [Platform((0,300-18),(100,18))]
        platforms += [Platform((800-90, 300-50), (100,50))]
        platforms += [Platform((0,0), (800,100))]
        run = True
        reset = False

    for player in players:
        if player.isEnemy and player.rectangle.colliderect(mainPlayer.rectangle):
            run = False
            
    if run:
        """if player.top > 400:
            run = False"""
        for player in players:
            player.impPlatforms = []

        for player in players:
            for platform in platforms:
                if minDistX(player.rectangle, platform.rectangle) <=5 or minDistY(player.rectangle, platform.rectangle)<= 20 or platform.rectangle.colliderect(player.rectangle)  :
                    player.impPlatforms += [platform]
        """
        for platform in platforms:
            platform.color = 'brown'

        for p in mainPlayer.impPlatforms:
            p.color = 'blue'
        """ 
        # move platform
        for platform in platforms:
            platform.rectangle.left -= mainPlayer.velocity

        for p in players:
            p.rectangle.left += p.velocity - mainPlayer.velocity
        
        
        # check for vertical hitting the platform
        for p in players:
            for platform in p.impPlatforms:
                if (p.gravity <= platform.rectangle.bottom - p.rectangle.top <= 1) and (platform.rectangle.left < p.rectangle.left < platform.rectangle.right or platform.rectangle.left < p.rectangle.right < platform.rectangle.right):
                        p.rectangle.top = platform.rectangle.bottom
                        p.gravity = -1 * p.gravity
        
        # check for collision in horizontal direction
        for p in players:
            for platform in p.impPlatforms:
                if  platform.rectangle.left < p.rectangle.right < platform.rectangle.right and p.rectangle.left < platform.rectangle.left:
                    if p.rectangle.colliderect(platform.rectangle): #p.rectangle.top < platform.rectangle.top < p.rectangle.bottom or p.rectangle.top < platform.rectangle.bottom < p.rectangle.bottom:
                        if not p.isEnemy:
                            for i in range(len(platforms)):
                                if platforms[i] != platform:
                                    platforms[i].rectangle.right += mainPlayer.rectangle.right - platform.rectangle.left
                            
                            for player in players:
                                if player.isEnemy:
                                   player.rectangle.right += mainPlayer.rectangle.right - platform.rectangle.left

                            platform.rectangle.left = mainPlayer.rectangle.right
                        else:
                            p.velocity *= -1
                elif platform.rectangle.left < p.rectangle.left < platform.rectangle.right and p.rectangle.right > platform.rectangle.right:
                    if p.rectangle.colliderect(platform.rectangle):#p.rectangle.top < platform.rectangle.top < p.rectangle.bottom or p.rectangle.top < platform.rectangle.bottom < p.rectangle.bottom:
                        if not p.isEnemy:
                            for i in range(len(platforms)):
                                if platforms[i] != platform:
                                    platforms[i].rectangle.right += mainPlayer.rectangle.left - platform.rectangle.right
                            
                            for player in players:
                                if player.isEnemy:
                                    player.rectangle.right += mainPlayer.rectangle.left - platform.rectangle.right

                            platform.rectangle.right = mainPlayer.rectangle.left
                        else:
                            p.velocity *= -1
        
        canJump = False
        
        # check for landing on platform
        for p in players:
            for platform in p.impPlatforms:
                if 0 <= - p.rectangle.bottom + platform.rectangle.top <= p.gravity and (platform.rectangle.left < p.rectangle.left < platform.rectangle.right or platform.rectangle.left < p.rectangle.right < platform.rectangle.right):
                    p.rectangle.bottom = platform.rectangle.top
                    if not p.isEnemy:
                        canJump = True
                    p.gravity = 0

        # effect of gravity and player movement
        for p in players:
            p.rectangle.top += p.gravity
            p.gravity += 1
        
    # event manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (canJump or (not run)):
                mainPlayer.gravity = -15
                mainPlayer.rectangle.top -= 1
            if event.key == pygame.K_RIGHT:
                mainPlayer.velocity = 5
            elif event.key == pygame.K_LEFT:
                mainPlayer.velocity = -5
            if not run:
                reset = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                mainPlayer.velocity = 0

    pygame.Surface.fill(screen, 'black')
    if run:
        for platform in platforms:
            platform.drawFloor(screen)

        # sprites
        if mainPlayer.gravity >= 0:
            if mainPlayer.velocity > 0:
                screen.blit(player_image, (mainPlayer.rectangle.left,mainPlayer.rectangle.top))
            elif mainPlayer.velocity <= 0:
                screen.blit(left_facing, (mainPlayer.rectangle.left,mainPlayer.rectangle.top))
        elif mainPlayer.gravity < 0:
            if mainPlayer.velocity > 0:
                screen.blit(jumping_right, (mainPlayer.rectangle.left,mainPlayer.rectangle.top))
            else:
                screen.blit(jumping_left, (mainPlayer.rectangle.left,mainPlayer.rectangle.top))
        for p in players:
            if p.isEnemy:
                p.drawPlayer(screen)
    else:
        screen.blit(text_surface, (100, 200))
    pygame.display.update()
    time.tick(60)

pygame.quit()
