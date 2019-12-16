import pygame
import os
import math
import random
pygame.mixer.init(16000, -16, 2, 2048)
pygame.init()


PADDLE_WIDTH = 80
# background_image = pygame.image.load("images/backgrounds/bakgrund-VS.jpg")

# windowsize = (pygame.display.Info().current_w-100, pygame.display.Info().current_h-100)
windowsize = (1320,740)
# print(pygame.display.Info())

win = pygame.display.set_mode(windowsize, pygame.FULLSCREEN)
pygame.display.set_caption("PONG - the classic game")
pygame.key.set_repeat(0, 500)


bounce = pygame.mixer.Sound(os.path.join('sounds','pool.ogg'))

wall_bounce = pygame.mixer.Sound(os.path.join('sounds','wall_bounce.ogg'))

# music_channel = pygame.mixer.find_channel()
# music_channel.play(pygame.mixer.Sound(os.path.join('sounds/music', 'PongSong.ogg')))
pygame.mixer.music.load(os.path.join('sounds/music', 'PongSong.ogg'))
pygame.mixer.music.play()

def play_wall_bounce():
    empty_channel = pygame.mixer.find_channel()
    # empty_channel.set_volume(0.5, 0.5)
    empty_channel.play(wall_bounce)

def play_bounce(direction):
    empty_channel = pygame.mixer.find_channel()
    if(empty_channel != None):
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

    def getSpeed(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2) #pythagoras sats <3

    def setSpeed(self,speed):
        self.speed = speed

    def getX(self):
        return self.coords[0]

    def getY(self):
        return self.coords[1]

    def setCoords(self,coords):
        self.coords = coords
    
    def setDimensions(self, dimensions):
        self.dimensions = dimensions

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

    bounces = 0

    def drawMe(self,surface):
        pygame.draw.circle(surface,self.color,(round(self.getX()),round(self.getY())),round(self.getWidth()/2.0))

    def addBounce(self, add=1):
        self.bounces = self.bounces + add
    
    def getBounces(self):
        return self.bounces
    
    def resetBounces(self):
        self.bounces = 0
    
    def randomAngle(self, wall=None):
        angle = random.uniform(0.17,math.pi-0.17) #random vinkel mellan 10-170 (omvandlat till radianer)
        if(wall == 1):  #förskjut vinkeln så att tekningen går mot angiven vägg; höger
            angle = angle - math.pi/2.0
        else:           #förskjut vinkeln så att tekningen går mot angiven vägg; vänster
            angle = angle + math.pi/2.0
        self.setStartAngle(angle)

    def setAngle(self,angle):
        """
        Tar emot vinkeln som räknas fram utefter var på paddeln bollen träffar paddeln. Träff längre ifrån
        centrum på paddeln ger högre vinkel.
        """
        # Krävs för att bollen skall studsar fram och tillbaka.
        # Gör att hastigheten i x-led växlar mellan positivt och negativt värde.
        angleaddon = math.pi
        if self.getSpeedX() < 0:
            angleaddon = 0
        
        # y är knutet till cos då cos-värdet är högre vid kantträff.
        newSpeed = (self.getSpeed()*math.sin(angle+angleaddon),self.getSpeed()*math.cos(angle))
        self.setSpeed(newSpeed)
        

    def setStartAngle(self, angle):
        newSpeed = (self.getSpeed()*math.cos(angle),self.getSpeed()*math.sin(angle))
        self.setSpeed(newSpeed)


class Status:
    statuscoords = (0,0)
    dimensions = (0,0)
    bgcolor = (0,0,0)

    def __init__(self, statuscoords=(300,0), dimensions=(100,200), bgcolor=(0,0,0), backgroundfile=None):
        self.statuscoords = statuscoords
        self.dimensions = dimensions
        self.bgcolor = bgcolor
        if(backgroundfile == None):
            self.me = pygame.image.load(os.path.join('images/backgrounds', 'field_black_1320x740.png'))
        else:
            self.me = pygame.image.load(os.path.join('images/backgrounds', backgroundfile))

    # def draw(self, surface):
    #     pygame.draw.rect(surface, self.bgcolor, [self.coords[0],self.coords[1],self.dimensions[0],self.dimensions[1]])

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
    """
    Gamestate = 0 --> SplashScreen
    Gamestate = 1 --> Game on!
    """
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
                    if(n==1):
                        self.score1=self.score1+1
                        self.faceOff(3)
                        self.ball.resetBounces()
                        for paddle in self.paddles:
                            paddle.setDimensions((10, PADDLE_WIDTH))
                    else:
                        self.score2=self.score2+1
                        self.faceOff(1)
                        for paddle in self.paddles:
                            paddle.setDimensions((10, PADDLE_WIDTH))
                else:
                    play_wall_bounce()
                    Ycoord = [wall.getY()+wall.getHeight(),0,wall.getY()-self.ball.getHeight(),0]
                    ball.setCoords((ball.getX(),Ycoord[n]))
                    self.ball.setSpeed((self.ball.getSpeedX(),(-1)*self.ball.getSpeedY()))
            n +=1
        n = 0
        for paddle in self.paddles:
            collideX, collideY = self.ball.collides(paddle)
            if(collideX and collideY):
                # self.ball.setSpeed(((-1)*self.ball.getSpeedX(),self.ball.getSpeedY()))
                ball_coords = (self.ball.getX(), self.ball.getY())
                paddle_coords = (paddle.getX(), paddle.getY())
                
                
                # Närliggande katet; bollens y-värde - paddelns y-värde i centrum som i nuläget ligger mellan -40 <= x <= 40
                # Delar detta med halva paddelns längd, i nuläget 40. Detta för att anpassa till enhetscirkeln.
                adjacent = float((ball_coords[1] - (paddle_coords[1]+paddle.getHeight()/2))/(paddle.getHeight()/2))

                # Ser till att inte få allt för extrema värden på närliggande katet.
                if adjacent > 0.9:
                    adjacent = 0.9
                elif adjacent < -0.9:
                    adjacent = -0.9
                
                # Är hypotenusan 1 ges vikeln av arccos(närliggande katet)
                angle = math.acos(adjacent)
                self.ball.setAngle(angle)

                self.ball.addBounce()

                if self.ball.getBounces() == 3:
                    paddle.setDimensions((10,paddle.getHeight()*0.85))
                if self.ball.getBounces() == 4:
                    paddle.setDimensions((10, paddle.getHeight()*0.85))
                    self.ball.resetBounces()

                

                if(n==0):
                    play_bounce('left')
                    self.ball.setCoords((paddle.getX()+paddle.getWidth(),self.ball.getY()))
                else:
                    play_bounce('right')
                    self.ball.setCoords((paddle.getX()-self.ball.getWidth(),self.ball.getY()))
            n += 1

    def faceOff(self,wall=None):
        if(wall == None):
            wall = random.randint(1,2)     #egentligen ska wall vara 1 eller 3, men if-satsen nedan bryr sig bara om ena värdet, så två funkar lika bra.
        self.ball.setCoords(((self.walls[1].getX()+self.walls[1].getWidth())/2.0,(self.walls[1].getY()+self.walls[1].getHeight())/2.0))
        self.ball.randomAngle(wall)

    def resetGame(self):
        self.faceOff()
        self.score1 = 0
        self.score2 = 0
        self.paddles[0].setCoords((5,windowsize[1]/2.0))  #player1, player2
        self.paddles[1].setCoords((windowsize[0]-15,windowsize[1]/2.0))
        self.ball.resetBounces()
        self.paddles[0].setDimensions((10, PADDLE_WIDTH))
        self.paddles[1].setDimensions((10, PADDLE_WIDTH))

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


ball = Ball(color=(255,0,0),dimensions=(10,10),coords=(windowsize[0]/2.0,windowsize[1]/2.0),speed=(5,5))
walls = []
walls.append(GameObject(color=(255,255,0),dimensions=(windowsize[0],100),coords=(0,-99)))   #top, right, bottom, left
walls.append(GameObject(color=(255,255,0),dimensions=(100,windowsize[1]),coords=(windowsize[0]-1,0)))
walls.append(GameObject(color=(255,255,0),dimensions=(windowsize[0],100),coords=(0,windowsize[1]-1)))
walls.append(GameObject(color=(255,255,0),dimensions=(100,windowsize[1]),coords=(-99,0)))
paddles = []
paddles.append(GameObject(color=(0,0,255),dimensions=(15,PADDLE_WIDTH),coords=(5,windowsize[1]/2.0),speed=(0.0,5.57)))  #player1, player2
paddles.append(GameObject(color=(0,255,0),dimensions=(15,PADDLE_WIDTH),coords=(windowsize[0]-15,windowsize[1]/2.0),speed=(0.0,5.57)))
rules = GameRules(ball,walls,paddles,0)
rules.faceOff()

theSplash = Status((0,0),(1320,768),(0,0,0),"splash.png")
theStatus = Status((10,10),(1300,720),(0,0,0))

theStatusContent = {
    "score1":   StatusContent(text=rules.getScore()[0], size=78, coords=(330,370)),
    "score2":   StatusContent(text=rules.getScore()[1], size=78, coords=(990,370)),
}

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                if(rules.gamestate == 0):
                    rules.gamestate = 1
                    rules.resetGame()
                else:
                    rules.gamestate = 0

        pygame.event.pump()

    win.fill((0,0,0))
    # win.blit(background_image, [0,0])
    if(rules.gamestate == 0):
        theSplash.draw(win)
    else:
        rules.keyPressed(pygame.key.get_pressed())
        rules.bounce()
        ball.move()
        theStatusContent["score1"].setText(rules.getScore()[0])
        theStatusContent["score2"].setText(rules.getScore()[1])
        theStatus.draw(win)
        for v in theStatusContent.values():
            v.draw(win)
        rules.draw(win)
    pygame.display.update()

pygame.quit()
