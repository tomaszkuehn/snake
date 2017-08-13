#snake Game

import pygame, sys, random, time, glob
from PIL import Image

check_errors = pygame.init()
if check_errors[1] > 0 :
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame succesfully initialized")

pygame.display.set_caption("Snake game")
playSurface = pygame.display.set_mode((720,460))

gamearena=[]
im = Image.open("gamearena.jpg")
col,row =  im.size
pixels = im.load()
for i in range(0,71):
    for j in range(0,45):
        r,g,b =  pixels[i,j]
        if r<50:
            gamearena.append([10*i,10*j])
        
#gamearena=[
#[200,200],[210,200],[220,200],[230,200],[230,210],[230,220],[240,220],[240,230],
#    [240,240],[240,250],[230,250],[220,250],[210,250],[200,250],[200,240],
#    [200,230],[200,220],[200,210]
#     
#]

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
brown = pygame.Color(165,42,42)

#sys.path.append('c:/')
#sys.path.append(os.basename(sys.argv[0]))
#crash_sound = pygame.mixer.Sound("C:\\sleep.mp3")

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
 
class food:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.ani_speed_init=10
        self.ani_speed=self.ani_speed_init
        self.ani = glob.glob("walk/doom_w*.png")
        self.ani.sort()
        self.ani_pos=0
        self.ani_max=len(self.ani)-1
        self.img = pygame.image.load(self.ani[0])
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
                self.img = pygame.image.load(self.ani[self.ani_pos])
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
    #if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
     #   foodSpawn = False
        #pygame.mixer.Sound.play(crash_sound)
      #  score +=1
    #else:
     #   snakeBody.pop()
    
    #if (abs(snakePos[0] - food1.x) < 10) and (abs(snakePos[1] - food1.y) < 10) :
     #   score +=1
      #  food1.randomize()
    #elif (abs(snakePos[0] - food2.x) < 10) and (abs(snakePos[1] - food2.y) < 10) :
     #   score +=1
      #  food2.randomize()
    #else:
     #   snakeBody.pop()
    
    #if foodSpawn == False:
     #   foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
    #foodSpawn = True
    
    scoremem = score
    for count in range (0,3):
        if (abs(snakePos[0] - foodlist[count].x) < 10) and (abs(snakePos[1] - foodlist[count].y) < 10) :
            score +=1
            foodlist[count].randomize()
    if scoremem == score:
        snakeBody.pop()
    
    playSurface.fill(white)
    
    isgameover = 0
    for pos in gamearena:
        pygame.draw.rect(playSurface, brown, pygame.Rect(pos[0]+0,pos[1]+0,10,10))
        if (abs(snakePos[0] - pos[0]) < 10) and (abs(snakePos[1] - pos[1]) < 10) :
            isgameover =1
    if isgameover == 1:
        gameOver()
        
    for pos in snakeBody:
        #pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
        pygame.draw.circle(playSurface, green, (pos[0]+0,pos[1]+0),5,0)
    
    #pygame.draw.circle(playSurface, brown, (foodPos[0]+0,foodPos[1]+0), 5,0)
    
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
    fpsController.tick(23)
    
    #print(repr(foodX)+" "+repr(foodY)+" | "+repr(snakePos[0])+" "+repr(snakePos[1]))

