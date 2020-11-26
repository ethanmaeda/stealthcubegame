#Ethan Maeda
#Stealth game
#Jun 1 added interactive start screen, fixed timer issue
#Jun 8 added rotating goal, started animation for player
#Jun 9 added player facing mechanics
#Jun 10 added tracking lasers
#Jun 11 cosmetic changes, preparing for new feature/item (?)
#Jun 12 added speed boost power-up and win, lose and power up sounds
#Jun 13 added harder difficulty where cameras move faster and there is no power-up

import pygame
import time
import math
from pygame.locals import *
import sys
pygame.init()
pygame.font.init()
pygame.mixer.init()
DISPLAY=(500, 800)
FPS=60
LIGHTGRAY=(170, 170, 170)
WHITE=(255, 255, 255)
YELLOW=(255, 255, 0)
RED=(255, 113, 113)
GREEN=(113, 255, 113)
BLACK=(0, 0, 0)
timeoffset=0 #For timer reset
angle=0 
timed=-2500 #For the timed boost power-up text
camspeed=2 

Surface = pygame.display.set_mode(DISPLAY)
clock=pygame.time.Clock()
font=pygame.font.Font("Roboto-Regular.ttf", 25)
fontbig=pygame.font.Font("Roboto-Regular.ttf", 35)

# Various boolean variables
toggleup=False
toggledown=False
toggleleft=False
toggleright=False

lookup=False
lookdown=False
lookleft=False
lookright=False

cam1down=True
cam1up=False
cam2down=False
cam2up=True
cam3right=True
cam3left=False

laserdown=True
laserup=False

brief=True
level1=False
lose1=False
win1=False
obtained=False

# Functions and classes
def CollisionCheck():
    if pygame.sprite.spritecollideany(player, nopassgroup)!= None:
        return True
    else:
        return False

class Entity(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        self.topleft=topleft
    def moveup(self, x):
        self.topleft[1]-=x
        self.rect=self.image.get_rect(topleft=self.topleft)
    def movedown(self, x):
        self.topleft[1]+=x
        self.rect=self.image.get_rect(topleft=self.topleft)
    def moveleft(self, x):
        self.topleft[0]-=x
        self.rect=self.image.get_rect(topleft=self.topleft)
    def moveright(self, x):
        self.topleft[0]+=x
        self.rect=self.image.get_rect(topleft=self.topleft)

class Player(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("player.png")
        self.rect=self.image.get_rect(topleft=self.topleft)
    def rotate(self, angle):
        self.newimage=pygame.transform.rotate(self.image, angle)
        self.rect=self.newimage.get_rect(topleft=self.topleft)
        
class Camera(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("camera.png")
        self.rect=self.image.get_rect(topleft=self.topleft)        
    def rotate(self, angle):
        self.newimage=pygame.transform.rotate(self.image, angle)
        self.rect=self.newimage.get_rect(topleft=self.topleft)
        
class WallLong(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("walllong.png")
        self.rect=self.image.get_rect(topleft=self.topleft)

class WallShort(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("wallshort.png")
        self.rect=self.image.get_rect(topleft=self.topleft)

class Island(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("island.png")
        self.rect=self.image.get_rect(topleft=self.topleft)

class Goal:
    def __init__(self, center):
        self.center=center
        self.image=pygame.image.load("goal.png")
        self.rect=self.image.get_rect(center=self.center)

class Laser(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("laser.png")
        self.rect=self.image.get_rect(topleft=self.topleft)

class PowerUp(Entity):
    def __init__(self, topleft):
        super().__init__(topleft)
        self.image=pygame.image.load("boost.png")
        self.rect=self.image.get_rect(topleft=self.topleft)

# Setting positions and grouping up unpassable entities
player=Player([30, 730])
boost=PowerUp([430, 730])
goal=Goal([412, 10])
camera1=Camera([90, 202])
camera2=Camera([290, 648])
camera3=Camera([90, 0])
wall1=WallLong([0, 0])
wall2=WallShort([DISPLAY[0]-90, DISPLAY[1]-700])
island1=Island([200, 100])
island2=Island([200, 300])
island3=Island([200, 500])
nopassgroup=pygame.sprite.Group()
nopassgroup.add(wall1, wall2, island1, island2, island3)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==pygame.K_w:
                toggleup=True
            if event.key==pygame.K_s:
                toggledown=True
            if event.key==pygame.K_d:
                toggleright=True
            if event.key==pygame.K_a:
                toggleleft=True
        if event.type==KEYUP:
            if event.key==pygame.K_w:
                toggleup=False
            if event.key==pygame.K_s:
                toggledown=False
            if event.key==pygame.K_d:
                toggleright=False
            if event.key==pygame.K_a:
                toggleleft=False
        if event.type==MOUSEBUTTONDOWN:      

# Briefing screen interaction and setting correct event
            if brief==True:
                if event.button==1:
                    if pygame.mouse.get_pos()[0] in range(int((500-startdim[0])/2), int((500-startdim[0])/2)+startdim[0]) and pygame.mouse.get_pos()[1] in range(450, int(450+startdim[1])):
                        lose1=False
                        win1=False
                        brief=False
                        level1=True
                        counter=0
                        camspeed=2
                        hard=False
                        timeoffset=pygame.time.get_ticks()

# Try again: resetting positions and variables and setting correct event 
            if lose1==True:
                if event.button==1:
                    if pygame.mouse.get_pos()[0] in range(int((500-tryagaindim[0])/2), int((500-tryagaindim[0])/2)+tryagaindim[0]) and pygame.mouse.get_pos()[1] in range(400, int(400+tryagaindim[1])):
                        lose1=False
                        win1=False
                        level1=True
                        counter=0
                        player=Player([25, 730])
                        goal=Goal([412, 10])
                        camera1=Camera([90, 202])
                        camera2=Camera([290, 648])
                        camera3=Camera([90, 0])
                        wall1=WallLong([0, 0])
                        wall2=WallShort([DISPLAY[0]-90, DISPLAY[1]-700])
                        island1=Island([200, 100])
                        island2=Island([200, 300])
                        island3=Island([200, 500])
                        nopassgroup=pygame.sprite.Group()
                        nopassgroup.add(wall1, wall2, island1, island2, island3)
                        obtained=False
                        if hard==True: 
                            speed=3
                            camspeed=3
                        else:
                            speed=3
                            camspeed=2
                        timed=-2500
                        timeoffset=pygame.time.get_ticks() #For resetting timer
# Play again on different difficulties: resetting positions and variables and setting correct event
            if win1==True:
                if event.button==1:
                    if pygame.mouse.get_pos()[0] in range(int((500-hardleveldim[0])/2), int((500-hardleveldim[0])/2)+hardleveldim[0]) and pygame.mouse.get_pos()[1] in range(500, int(500+hardleveldim[1])):
                        win1=False
                        lose1=False
                        level1=True
                        hard=True
                        counter=0
                        player=Player([25, 730])
                        goal=Goal([412, 10])
                        camera1=Camera([90, 202])
                        camera2=Camera([290, 648])
                        camera3=Camera([90, 0])
                        wall1=WallLong([0, 0])
                        wall2=WallShort([DISPLAY[0]-90, DISPLAY[1]-700])
                        island1=Island([200, 100])
                        island2=Island([200, 300])
                        island3=Island([200, 500])
                        nopassgroup=pygame.sprite.Group()
                        nopassgroup.add(wall1, wall2, island1, island2, island3)
                        obtained=False
                        camspeed=3.3
                        speed=3
                        timed=-2500
                        timeoffset=pygame.time.get_ticks() #For resetting timer
                    if pygame.mouse.get_pos()[0] in range(int((500-easyleveldim[0])/2), int((500-easyleveldim[0])/2)+easyleveldim[0]) and pygame.mouse.get_pos()[1] in range(550, int(550+easyleveldim[1])):
                        win1=False
                        lose1=False
                        level1=True
                        hard=False
                        counter=0
                        player=Player([25, 730])
                        goal=Goal([412, 10])
                        camera1=Camera([90, 202])
                        camera2=Camera([290, 648])
                        camera3=Camera([90, 0])
                        wall1=WallLong([0, 0])
                        wall2=WallShort([DISPLAY[0]-90, DISPLAY[1]-700])
                        island1=Island([200, 100])
                        island2=Island([200, 300])
                        island3=Island([200, 500])
                        nopassgroup=pygame.sprite.Group()
                        nopassgroup.add(wall1, wall2, island1, island2, island3)
                        obtained=False
                        camspeed=2
                        timed=-2500
                        timeoffset=pygame.time.get_ticks() #For resetting timer

# Pre-game briefing event            
    if brief==True:
        Surface.fill(BLACK)
        briefing1=font.render("Reach the orange goal", True, WHITE)
        briefing2=font.render("Don't get caught by the cameras or lasers", True, WHITE)
        briefing3=font.render("Try and get a fast time!", True, WHITE)
        briefing4=font.render("Use WASD to move the blue character", True, WHITE)
        briefing5=font.render("Look for power-ups", True, WHITE)
        briefing1dim=font.size("Reach the orange goal")
        briefing2dim=font.size("Don't get caught by the cameras or lasers")
        briefing3dim=font.size("Try and get a fast time!")
        briefing4dim=font.size("Use WASD to move the blue character")
        briefing5dim=font.size("Look for power-ups")
        start=fontbig.render("Click here when ready to start", True, YELLOW)
        startdim=fontbig.size("Click here when ready to start")
        Surface.blit(briefing1, ((500-briefing1dim[0])/2, 150))
        Surface.blit(briefing2, ((500-briefing2dim[0])/2, 200))
        Surface.blit(briefing3, ((500-briefing3dim[0])/2, 250))
        Surface.blit(briefing4, ((500-briefing4dim[0])/2, 300))
        Surface.blit(briefing5, ((500-briefing5dim[0])/2, 350))
        Surface.blit(start, ((500-startdim[0])/2, 450))

# Win screen event
    if win1==True: 
        level1=False
        lose1=False
        Surface.fill(GREEN)
        text1=font.render("Congratulations!", True, BLACK)
        text1dim=font.size("Congratulations")
        timetext=font.render("Your time was: "+str(finaltime), True, BLACK)
        timetextdim=font.size("Your time was: "+str(finaltime))
        hardlevel=font.render("Click here to play again on harder difficulty", True, BLACK)
        hardleveldim=font.size("Click here to play again on harder difficulty")
        easylevel=font.render("Click here to play again on easy difficulty", True, BLACK)
        easyleveldim=font.size("Click here to play again on easy difficulty")
        Surface.blit(text1, ((500-text1dim[0])/2, 300))
        Surface.blit(timetext, ((500-timetextdim[0])/2, 400))
        Surface.blit(hardlevel, ((500-hardleveldim[0])/2, 500))
        Surface.blit(easylevel, ((500-easyleveldim[0])/2, 550))

# Lose screen event
    if lose1==True:
        level1=False
        win1=False
        Surface.fill(RED)
        text1=font.render("You lost!", True, BLACK)
        text1dim=font.size("You lost!")
        Surface.blit(text1, ((500-text1dim[0])/2, 300))
        tryagain=fontbig.render("Click here to try again", True, BLACK)
        tryagaindim=fontbig.size("Click here to try again")
        Surface.blit(tryagain, ((500-tryagaindim[0])/2, 400))

########### LEVEL 1 ############ 
    if level1==True:

# Blitting
        Surface.fill(LIGHTGRAY)
        Surface.blit(camera1.image, camera1.topleft)
        camera2.rotate(180)
        Surface.blit(camera2.newimage, camera2.rect)
        camera3.rotate(-90)
        Surface.blit(camera3.newimage, camera3.rect)

# Laser timers and blitting
        if counter==380:
            counter=0
        else:
            counter+=1

        if counter<190:
            laser1=Laser([248, 200])
            laser2=Laser([0, 0])
            laser3=Laser([410, 700])
            Surface.blit(laser1.image, laser1.topleft)
            Surface.blit(laser3.image, laser3.topleft)
        elif counter>190:
            laser1=Laser([0, 0])
            laser2=Laser([248, 400])
            laser3=Laser([0, 0])
            Surface.blit(laser2.image, laser2.topleft)   

        nopassgroup.draw(Surface)

# Player facing direction blitting
        if toggleup==True and toggleright==True:
            player.rotate(45)
            Surface.blit(player.newimage, player.rect)
        elif toggleup==True and toggleleft==True:
            player.rotate(135)
            Surface.blit(player.newimage, player.rect)
        elif toggledown==True and toggleright==True:
            player.rotate(-45)
            Surface.blit(player.newimage, player.rect)
        elif toggledown==True and toggleleft==True:
            player.rotate(-135)
            Surface.blit(player.newimage, player.rect)
        elif lookup==True:
            player.rotate(90)
            Surface.blit(player.newimage, player.rect)
        elif lookdown==True:
            player.rotate(-90)
            Surface.blit(player.newimage, player.rect)
        elif lookright==True:
            Surface.blit(player.image, player.topleft)
        elif lookleft==True:
            player.rotate(180)
            Surface.blit(player.newimage, player.rect)
        else:
            Surface.blit(player.image, player.topleft)
            
# Rotating goal blitting
        rotategoal=pygame.transform.rotate(goal.image, angle)
        new_rect=rotategoal.get_rect(center=(450, 45))
        Surface.blit(rotategoal, new_rect)
        angle+=5

# Timer blitting
        timertext=font.render(str((pygame.time.get_ticks()-timeoffset)/1000), True, WHITE)
        Surface.blit(timertext, (5, 0))

# Conditions for contact with cameras, lasers and goal
        enemies=[camera1, camera2, camera3, laser1, laser2, laser3]
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy) == True:
                lose1=True
                pygame.mixer.music.load("lose.mp3")
                pygame.mixer.music.play(0)
        if pygame.sprite.collide_rect(player, goal) == True:
            win1=True
            pygame.mixer.music.load("win.ogg")
            pygame.mixer.music.play(0)
            finaltime="{:.3f}".format((pygame.time.get_ticks()-timeoffset)/1000) 

# Conditions for contact with boost power up and updates
        if hard==False: 
            if pygame.sprite.collide_rect(player, boost) == True:
                pygame.mixer.music.load("powerup.mp3")
                pygame.mixer.music.play(0)
                boost=PowerUp([0, 0])
                speed=5
                obtained=True
                obtainedtext=font.render("You have increased speed", True, WHITE)
                obtainedtextdim=font.size("You have increased speed")
                timed=pygame.time.get_ticks()
            if timed+2500>pygame.time.get_ticks():
                Surface.blit(obtainedtext, (0, 750))
            if obtained==False:
                boost=PowerUp([440, 730])
                speed=3
                Surface.blit(boost.image, boost.rect)

# Collision with unpassable check and player movement    
        if toggleup==True:
            lookup=True
            lookdown=False
            lookright=False
            lookleft=False
            if player.topleft [1]>0:
                player.moveup(speed)
                if CollisionCheck()==True:
                    player.movedown(speed)
        if toggledown==True:
            lookup=False
            lookdown=True
            lookright=False
            lookleft=False
            if player.topleft[1]<DISPLAY[1]-50:
                player.movedown(speed)
                if CollisionCheck()==True:
                    player.moveup(speed)
        if toggleright==True:
            lookup=False
            lookdown=False
            lookright=True
            lookleft=False
            if player.topleft[0]<DISPLAY[0]-50:
                player.moveright(speed)
                if CollisionCheck()==True:
                    player.moveleft(speed)
        if toggleleft==True:
            lookup=False
            lookdown=False
            lookright=False
            lookleft=True
            if player.topleft[0]>0:
                player.moveleft(speed)
                if CollisionCheck()==True:
                    player.moveright(speed)

# Camera movement
        if cam1down==True:
            if camera1.topleft[1]<648:
                camera1.movedown(camspeed)
            else:
                cam1down=False
                cam1up=True
        if cam1up==True:
            if camera1.topleft[1]>202:
                camera1.moveup(camspeed)
            else:
                cam1up=False
                cam1down=True
        if cam2down==True:
            if camera2.topleft[1]<648:
                camera2.movedown(camspeed)
            else:
                cam2down=False
                cam2up=True
        if cam2up==True:
            if camera2.topleft[1]>202:
                camera2.moveup(camspeed)
            else:
                cam2up=False      
                cam2down=True
        if cam3right==True:
            if camera3.topleft[0]<350:
                camera3.moveright(camspeed)
            else:
                cam3right=False
                cam3left=True
        if cam3left==True:
            if camera3.topleft[0]>90:
                camera3.moveleft(camspeed)
            else:
                cam3right=True
                cam3left=False  

#Display update and clock
    pygame.display.update()
    clock.tick(FPS)
