import pygame,sys
from threading import Timer
import random
pygame.init()
width,height=600,400
screen=pygame.display.set_mode((width,height))
bg=pygame.image.load('img/bg.jpg').convert()
bg=pygame.transform.smoothscale(bg,(width,height))
menu=pygame.image.load('img/menu.jpg').convert()
menu=pygame.transform.smoothscale(menu,(width,height))
ground=pygame.image.load('img/ground.png').convert()
groundY=50
ground=pygame.transform.smoothscale(ground,(width*2,groundY))
groundY=height-groundY
groundX=0
bird=pygame.image.load('img/bird.png').convert_alpha()
bird_width,bird_height=40,30
bird=pygame.transform.smoothscale(bird,(bird_width,bird_height))
pipe_up=pygame.image.load('img/pipe_up.png').convert_alpha()
pipe_down=pygame.image.load('img/pipe_down.png').convert_alpha()
bird_pos_x=90
bird_pos_y=height/2-bird_height
spd=0.8
began=False
hopp=50
drop_spd=0.4
drop_mul=1.03
pipe=[]
pipe_width=90
pipe_space=115
pipeTimer=300
pipeCount=300
bird_angle=0
ng=False    
running=True
pipe_countdown=None
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
new_game = myfont.render('click to play', False, (0, 0, 0))
point=0
text_color=(0,0,0)
clock=pygame.time.Clock()
def random_rgb():
    global text_color
    text_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def handle_hopp():
    global bird_pos_y,drop_spd,drop_mul,bird_angle
    bird_pos_y-=hopp
    drop_spd=0.8
    drop_mul=1.032
    bird_angle=50
def bird_handle():
    global drop_spd,drop_mul, bird_pos_y,bird_angle
    drop_spd*=drop_mul
    bird_pos_y+=drop_spd
    if bird_angle>=-50:
        bird_angle-=drop_spd 
def draw_bird():
    global bird
    screen.blit(pygame.transform.rotate(bird,bird_angle),(bird_pos_x,bird_pos_y))
def spd_bg_handle():
    global width,groundX
    if groundX>-width:
        groundX-=spd
    else:
        groundX=0
def spd_pipe_handle():
    global pipe
    for i in pipe:
        i[0]-=spd
def check_begin():
    global began
    began=True
def pipe_make():
    global pipe,pipeCount
    if began==True:
        if pipeCount==pipeTimer:
            pipeCount=0
            pipe_height=random.randint(40,groundY-100)
            pipe+=[[width,pipe_height,
                pipe_height+pipe_space,
                height-(pipe_height+pipe_space),
                pygame.transform.smoothscale(pipe_down,(pipe_width,pipe_height)),
                pygame.transform.smoothscale(pipe_up,(pipe_width,height-(pipe_height+pipe_space)))]]
        else :
            pipeCount+=1
    
def draw_pipe():
    for e in pipe:
        pipe_downc=e[4]
        pipe_upc=e[5]
        screen.blit(pipe_downc,(e[0],0))
        screen.blit(pipe_upc,(e[0],e[2]))
    
def pipe_delete():
    global pipe
    if len(pipe)>0 and pipe[0][0]+pipe_width<0:
        pipe.pop(0)
def draw_point():
    global point
    if len(pipe)>0 and pipe[0][0]>=bird_pos_x-spd and pipe[0][0]<bird_pos_x:
        point+=1
        random_rgb()
    point_img = myfont.render(str(point), False, text_color)
    screen.blit(point_img,(width/2-15*len(str(point)),50))
def check_lose():
    global ng,pipe,point
    if len(pipe)>0 and bird_pos_x+bird_width>pipe[0][0] and bird_pos_x<pipe[0][0]+pipe_width:
        if bird_pos_y<pipe[0][1]-30 or bird_pos_y+bird_height>pipe[0][2]:
            ng=False
            pipe=[]
            point=0
    return
def main(events):
    global bird_pos_y
    for e in events:
        if e.type==pygame.KEYDOWN and e.key == pygame.K_SPACE or e.type==pygame.MOUSEBUTTONUP:
            if bird_pos_y>=0 :handle_hopp()
            check_begin()
    spd_bg_handle()
    spd_pipe_handle()
    pipe_make()
    pipe_delete()
    if began==True and bird_pos_y+bird_height<=groundY:
        check_lose() 
        bird_handle()
    if bird_pos_y+bird_height>groundY:bird_pos_y=groundY-bird_height
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundX,groundY))
    draw_pipe()
    draw_point()
    draw_bird()
def menuF():
    global ng
    while True:
        events=pygame.event.get()
        for e in events:
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type==pygame.KEYDOWN or e.type==pygame.MOUSEBUTTONUP:
                if ng==False:
                    ng=True
        if ng:
            main(events)
        else:    
            screen.blit(menu,(0,0))
            screen.blit(new_game,(width/3+10,height-100))
        pygame.display.update()
        clock.tick(120)
menuF()
