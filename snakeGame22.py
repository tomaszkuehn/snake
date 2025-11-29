#snake Game

import pygame, sys, random, time, glob
from PIL import Image

check_errors = pygame.init()
if check_errors[1] > 0 :
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame succesfully initialized")

pygame.display.set_caption("Snake game on steroids")
playSurface = pygame.display.set_mode((720,460))

gamearena=[]
im = Image.open("gamearena.jpg")
mode = im.mode
size = im.size
data = im.tobytes()
imp = pygame.image.fromstring(data, size, mode)
col,row =  im.size
pixels = im.load()
for i in range(0,71):
    for j in range(0,45):
        sumr = 0
        for x in range(0,7):
            for y in range(0,7):
                r,g,b =  pixels[10*i+x,10*j+y]
                sumr = sumr + r
        if sumr<10200:
            gamearena.append([10*i,10*j])

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
brown = pygame.Color(165,42,42)

#FPS
fpsController = pygame.time.Clock()

snakePos = [100,50]
snakeBody = [[100,50],[90,50],[80,50]]

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction
score = 0

#Game over
def gameOver():
    myFont = pygame.font.SysFont('monaco',72)
    GOsurf = myFont.render('Game over!',True,red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360,15)
    playSurface.blit(GOsurf,GOrect)
    showScore()
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()
    
def showScore():
    sFont = pygame.font.SysFont('monaco',24)
    Ssurf = sFont.render('Score : {0}'.format(score),True,black)
    Srect = Ssurf.get_rect()
    Srect.midtop = (60,20)
    playSurface.blit(Ssurf,Srect)
    
def showStart():
    sFont = pygame.font.SysFont('monaco',72)
    Ssurf = sFont.render('Hit any key to start Snake',True,red)
    Srect = Ssurf.get_rect()
    Srect.midtop = (360,240)
    playSurface.blit(Ssurf,Srect) 
    sFont = pygame.font.SysFont('monaco',25)
    Ssurf = sFont.render('Control snake with A-S-D-W keys',True,red)
    Srect = Ssurf.get_rect()
    Srect.midtop = (560,290)
    playSurface.blit(Ssurf,Srect)
 
class food:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.ani_speed_init=10
        self.ani_speed=self.ani_speed_init
        files = glob.glob("walk/doom_w*.png")
        files.sort()
        self.ani = [pygame.image.load(f).convert_alpha() for f in files]
        self.ani_pos=0
        self.ani_max=len(self.ani)-1
        self.img = self.ani[0]
        self.dir = 1
        self.HV = 1
        self.update(0,0)
        
    def randomize(self):
        self.x = random.randrange(100,620)
        self.y = random.randrange(100,360)
        self.update(0,0)

    def update(self, posX, posY):
        if True:
            self.ani_speed-=1
            self.x+=2*posX
            self.y+=2*posY
            
            if self.x >700:
                self.x = 700
                self.dir = -self.dir    
            if self.y >440:
                self.y = 440
                self.dir = -self.dir 
            if self.x <10:
                self.x = 10
                self.dir = -self.dir 
            if self.y <10:
                self.y =10
                self.dir = -self.dir 
            
            if self.ani_speed == 0:
                self.img = self.ani[self.ani_pos]
                self.ani_speed = self.ani_speed_init
                if self.ani_pos == self.ani_max:
                    self.ani_pos=0
                else:
                    self.ani_pos+=1
        #print(self.ani_pos)
        playSurface.blit(self.img,(self.x-25,self.y-20))
        pygame.draw.circle(playSurface, black, (self.x,self.y), 6,0)
        

foodlist=[]
foodlist.append(food())
foodlist.append(food())
foodlist.append(food())

for count in range(0,3):
    foodlist[count].randomize()
    
playSurface.blit(imp,(0,0))
showStart()
pygame.display.flip()
waitkey = 1
while waitkey:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waitkey = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUIT")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_RIGHT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_RIGHT or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
        
    if direction == 'RIGHT':
        snakePos[0] += 5
    if direction == 'LEFT':
        snakePos[0] -= 5
    if direction == 'UP':
        snakePos[1] -= 5
    if direction == 'DOWN':
        snakePos[1] += 5
        
    snakeBody.insert(0,list(snakePos))
    
    scoremem = score
    for count in range (0,3):
        if (abs(snakePos[0] - foodlist[count].x) < 20) and (abs(snakePos[1] - foodlist[count].y) < 20) :
            score +=1
            foodlist[count].randomize()
    if scoremem == score:
        snakeBody.pop()
    
    #playSurface.fill(white)
    playSurface.blit(imp,(0,0))
    
    isgameover = 0
    for pos in gamearena:
        #pygame.draw.rect(playSurface, brown, pygame.Rect(pos[0]+0,pos[1]+0,10,10))
        if (abs(snakePos[0] - pos[0]) < 10) and (abs(snakePos[1] - pos[1]) < 10) :
            isgameover =1
    if isgameover == 1:
        gameOver()
        
    for pos in snakeBody:
        pygame.draw.circle(playSurface, green, (pos[0]+0,pos[1]+0),5,0)
    
    
    if snakePos[0] > 710 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()    
        
    showScore()
    
    for count in range(0,3):
        rr = random.randrange(1,100)
        if rr<3 :
            foodlist[count].HV = 1 -foodlist[count].HV    
        if(rr<2):
            foodlist[count].dir =  -foodlist[count].dir
        if foodlist[count].HV:
            foodlist[count].update(foodlist[count].dir,0)
        else:
            foodlist[count].update(0,foodlist[count].dir)

    pygame.display.flip()
    fpsController.tick(15)

