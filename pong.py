import pygame
import os
pygame.mixer.init(22100, -16, 2, 256)
pygame.init()

background_image = pygame.image.load("images/backgrounds/bakgrund-VS.jpg")

# windowsize = (pygame.display.Info().current_w-100, pygame.display.Info().current_h-100)
windowsize = (1000,636)
# print(pygame.display.Info())

win = pygame.display.set_mode(windowsize)
pygame.display.set_caption("PONG - the classic game")
pygame.key.set_repeat(0, 500)
bounce = pygame.mixer.Sound(os.path.join('sounds','pool.ogg'))

def play_bounce(direction):
    empty_channel = pygame.mixer.find_channel()
    if direction == 'left':
        empty_channel.set_volume(1.0,0.0)
    else:
        empty_channel.set_volume(0.0,1.0)
    empty_channel.play(bounce)

class GameObject:
    def __init__(self,color=(0,0,0),dimensions=(10,10),coords=(0,0), speed=(0.0,0.0)):
        self.color = color
        self.dimensions = dimensions
        self.coords = coords
        self.speed = speed

    def getSpeedX(self):
        return self.speed[0]
  
    def getSpeedY(self):
        return self.speed[1]
  
    def setSpeed(self,speed):
        self.speed = speed
  
    def getX(self):
        return self.coords[0]
  
    def getY(self):
        return self.coords[1]

    def setCoords(self,coords):
        self.coords = coords

    def getWidth(self):
        return self.dimensions[0]

    def getHeight(self):
        return self.dimensions[1]
  
    def drawMe(self,surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(round(self.getX()), round(self.getY()), self.getWidth(), self.getHeight()))
  
    def move(self):
        coords = list(self.coords)
        coords[0] = self.coords[0] + self.speed[0]
        coords[1] = self.coords[1] + self.speed[1]
        self.coords = tuple(coords)

    def collides(self,otherObject):
        collideX = False
        collideY = False
        if(self.getX()+self.getWidth()>otherObject.getX() and self.getX()<=otherObject.getX()+otherObject.getWidth()):
            collideX = True
        if(self.getY()+self.getHeight()>otherObject.getY() and self.getY()<=otherObject.getY()+otherObject.getHeight()):
            collideY = True
        return collideX, collideY

class Ball(GameObject):
    def drawMe(self,surface):
        pygame.draw.circle(surface,self.color,(round(self.getX()),round(self.getY())),round(self.getWidth()/2.0))

class Status:
    statuscoords = (0,0)
    dimensions = (0,0)
    bgcolor = (0,0,0)
    me = pygame.image.load(os.path.join('images/backgrounds', 'field_black_1000x636.png'))

    def __init__(self, statuscoords=(300,0), dimensions=(100,200), bgcolor=(0,0,0)):
        self.statuscoords = statuscoords
        self.dimensions = dimensions
        self.bgcolor = bgcolor

    def draw(self, surface):
        pygame.draw.rect(surface, self.bgcolor, [self.coords[0],self.coords[1],self.dimensions[0],self.dimensions[1]])

    def draw(self,surface):
        surface.blit(self.me, (self.statuscoords[0],self.statuscoords[1]))
        #return self.me

    def coords(self):
        return (self.statuscoords[0],self.statuscoords[1])

class StatusContent:
    textArray = []
    size = 12
    def __init__(self, text="",size=12,color = (255,255,255),coords=(0,0),bold=False,italic=False):
        self.setText(text)
        self.size = size
        self.color = color
        self.statcoords = coords
        self.bold = bold
        self.italic = italic
        self.fontobj = pygame.font.SysFont("sans serif",self.size,self.bold,self.italic)

    def draw(self,surface):
        n = 0
        for text in self.textArray:
            TextSurface = self.fontobj.render(text, True, self.color)
            surface.blit(TextSurface, (self.statcoords[0],self.statcoords[1]+n*self.size))
            n += 1

    def coords(self):
        return self.statcoords
    
    def setText(self,text):
        if text.find("\n") > -1:
            self.textArray = text.split("\n")
            n = 0
            for text in self.textArray:
                self.textArray[n] = text.strip()
                n += 1
        else:
            self.textArray = [text]

class GameRules():
    def __init__(self,ball,walls,paddles,gamestate = 0):
        self.score1=0
        self.score2=0
        self.ball = ball
        self.walls = walls
        self.paddles = paddles
        self.p1Keys = [pygame.K_w,pygame.K_s]   #keys as up,down
        self.p2Keys = [pygame.K_i,pygame.K_k]
        self.gamestate = gamestate
        
    def bounce(self):
        n = 0
        for wall in self.walls:
            collideX, collideY = self.ball.collides(wall)
            if(collideX and collideY):
                if(n==1 or n==3):    #if walls right or left don´t bounce - do score thingy
                    self.ball.setCoords(((self.walls[1].getX()+self.walls[1].getWidth())/2.0,(self.walls[1].getY()+self.walls[1].getHeight())/2.0))
                    if(n==1):
                        self.score1=self.score1+1
                        
                    else:
                        self.score2=self.score2+1
                        
                else:
                    Ycoord = [wall.getY()+wall.getHeight(),0,wall.getY()-self.ball.getHeight(),0]
                    ball.setCoords((ball.getX(),Ycoord[n]))
                    self.ball.setSpeed((self.ball.getSpeedX(),(-1)*self.ball.getSpeedY()))
            n +=1
        n = 0
        for paddle in self.paddles:
            collideX, collideY = self.ball.collides(paddle)
            if(collideX and collideY):
                self.ball.setSpeed(((-1)*self.ball.getSpeedX(),self.ball.getSpeedY()))
                if(n==0):
                    play_bounce('left')
                    ball.setCoords((paddle.getX()+paddle.getWidth(),self.ball.getY()))
                else:
                    play_bounce('right')
                    ball.setCoords((paddle.getX()-self.ball.getWidth(),self.ball.getY()))
            n += 1
    
    def getScore(self):
        return str(self.score1), str(self.score2)
                
    def keyPressed(self, keys):
        available_keys = self.p1Keys+self.p2Keys
        for key in available_keys:
            if keys[key]:
                if(available_keys.index(key) > 1): #choose the right paddle to move
                    p = 1
                else:
                    p = 0
                k = (available_keys.index(key)%2)+1    #translates 0 and 2 to 1 and 1 and 3 to 2 so that the directional minus will be correct
                direction = (-1)**k
                self.paddles[p].setSpeed((self.paddles[p].getSpeedX(),direction*abs(self.paddles[p].getSpeedY())))
                self.paddles[p].move()
                collideX, collideY = self.paddles[p].collides(self.walls[0])
                if(collideY):
                    self.paddles[p].setCoords((self.paddles[p].getX(),self.walls[0].getY()+self.walls[0].getHeight()))
                collideX, collideY = self.paddles[p].collides(self.walls[2])
                if(collideY):
                    self.paddles[p].setCoords((self.paddles[p].getX(),self.walls[2].getY()-self.paddles[p].getHeight()))
                
    def draw(self,surface):
        for obj in walls+paddles+[ball]:
            obj.drawMe(surface)
        
        
ball = Ball(color=(255,0,0),dimensions=(10,10),coords=(windowsize[0]/2.0,windowsize[1]/2.0),speed=(1.75,1.75))
walls = []
walls.append(GameObject(color=(255,255,0),dimensions=(windowsize[0],1),coords=(0,0)))   #top, right, bottom, left
walls.append(GameObject(color=(255,255,0),dimensions=(1,windowsize[1]),coords=(windowsize[0]-1,0)))
walls.append(GameObject(color=(255,255,0),dimensions=(windowsize[0],1),coords=(0,windowsize[1]-1)))
walls.append(GameObject(color=(255,255,0),dimensions=(1,windowsize[1]),coords=(0,0)))
paddles = []
paddles.append(GameObject(color=(0,0,255),dimensions=(10,40),coords=(0,windowsize[1]/2.0),speed=(0.0,1.57)))  #player1, player2
paddles.append(GameObject(color=(0,255,0),dimensions=(10,40),coords=(windowsize[0]-10,windowsize[1]/2.0),speed=(0.0,1.57)))
rules = GameRules(ball,walls,paddles,1)

theStatus = Status((0,0),(1000,636),(0,0,0))

print("score1:")
print(rules.getScore()[0])

theStatusContent = {
    "score1":   StatusContent(text=rules.getScore()[0], size=78, coords=(250,300)),
    "score2":   StatusContent(text=rules.getScore()[1], size=78, coords=(750,300)),
}

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        pygame.event.pump()

    rules.keyPressed(pygame.key.get_pressed())
    rules.bounce()
    ball.move()

    win.fill((0,0,0))
    # win.blit(background_image, [0,0])
    theStatusContent["score1"].setText(rules.getScore()[0])
    theStatusContent["score2"].setText(rules.getScore()[1])
    theStatus.draw(win)
    for v in theStatusContent.values():
        v.draw(win)
    rules.draw(win)
    pygame.display.update()

pygame.quit()
    
