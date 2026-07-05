#!/usr/bin/python
"""
 * Example_RoboticArm.py
 * Created on: 31 May 2026
 * Improved for: 31 May 2026
 * Author: Guy and Tzur Soffer
 * Copyright (C) 2026 Guy Soffer
"""
import math
import pygame
import RoboticArm_Class
from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame
from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
from GSOF_3dWireFrame.Lib3D.Utils import Colors
from GSOF_3dWireFrame.Lib3D import Objects
from GSOF_3dWireFrame.Lib3D import WireFrame_display as DISP

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
pygame.init()

def clearScreen(screen, color=Colors.WHITE) -> None:
  screen.fill(color)

def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=Colors.WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen

def rotateFromMouse(obj):
    (mPosX, mPosY) = pygame.mouse.get_pos()
    camAngY_r = 0.01*(mPosX -SCREEN_WIDTH/2)
    camAngX_r = 0.01*(mPosY -SCREEN_HEIGHT/2)
    obj.transform(rotate=(camAngX_r,camAngY_r,0), translate=(0,0,-1000))

if __name__ == "__main__":
    ground = Object_wireFrame(
        obj=Objects.net(250,250), color=Colors.GRAY)\
        .rotate(x=math.pi/2, y=0, z=0)\
        .scale(1.0)\
        .translate(-1500, 0, -2500)\
        .setOrigin()

    roboticArm = RoboticArm_Class.View()
    roboticArm.rotate(x=-0*math.pi/4, y=0, z=0).translate(-132, 0, 0).setOrigin()
    
    mouse = Object_wireFrame(
        obj=Objects.sphere(2), color=Colors.RED)\
        .scale(5.0)\
        .setOrigin()

    world = Assembly(objects=(ground, roboticArm, mouse)).translate(x=0, y=-300, z=-2200).setOrigin()

    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, Colors.WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=1, scale=1000.0)

    fps = 30
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        clearScreen(screen, Colors.DARK_BLUE)
        world.reset()
        
        mx, my = pygame.mouse.get_pos()
        mPosX = 2000*2*(mx/SCREEN_WIDTH -0.5)         #< Left negative
        mPosY = 1000*(-2)*(my/SCREEN_HEIGHT -0.5)+300 #< Up positive
        mPosZ = 300
        
        #print(mPosX, mPosY, mPosZ)
        roboticArm.moveTo(mPosX, mPosY, mPosZ)
        mouse.translate(mPosX, mPosY, mPosZ)

        # roboticArm.setArmAngles(
        #     base=math.pi/2,
        #     angle1=0,
        #     angle2=0,
        #     angle3=math.pi/4
        # )

        wireframe.draw(world)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
