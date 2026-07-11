#!/usr/bin/python
"""
 * RoboticArm_Class.py
 * Created on: 27 June 2026
 * Improved for: 27 june 2026
 * Author: Tzur and Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
import copy
import math
try:
    from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
    from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
    from GSOF_3dWireFrame.Lib3D.Utils import Colors
except:
    raise "GSOF_Wireframe3D module isn't installed"

class View(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        baseObj = Object(
            filename="%s/RobotArm/Base.stl"%folder, color=Colors.BLUE)\
            .rotate(-math.pi/2, 0, 0)\
            .translate(132, -200, 0)\
            .scale(0.3)\
            .setOrigin()
        armObj = Object(
            filename="%s/RobotArm/Arm.stl"%folder, color=Colors.YELLOW)\
            .rotate(math.pi/2, 0, 0)\
            .scale(0.3)\
            .setCenter(scale=1.0, method="arithCenter")\
            .setOrigin()
        
        dot = Object(
            filename="%s/RobotArm/cube.json"%folder, color=Colors.RED)\
            .scale(3)\
            .translate(-50+135, 200, 0)\
            .setOrigin()

        self.armLength = 300
        self.arm1 = Assembly(objects=(copy.deepcopy(armObj),))
        self.arm2 = Assembly(objects=(copy.deepcopy(armObj), Assembly(objects=(self.arm1,)).translate(-self.armLength, 0, 0).setOrigin()))
        self.arm3 = Assembly(objects=(copy.deepcopy(armObj), Assembly(objects=(self.arm2,)).translate(-self.armLength, 0, 0).setOrigin()))
        self._rotateArm(self.arm3, -math.pi/2).setOrigin()

        self.robot = Assembly(objects=(baseObj, self.arm3))

        super().__init__(objects=(self.robot, dot))

    def _rotateArm(self, arm:Assembly, angle:float|int, center=(135, 0, 0)):
        arm.rotate(x=0, y=0, z=angle, centerAt=center)
        return arm

    def _getHeading(self, targetX, targetZ) -> float:
        return math.atan2(targetX, targetZ) +math.pi/2
    
    def _getElevation(self, targetX, targetY) -> float:
        return math.pi/2 -math.atan2(targetY, abs(targetX)) 

    def _getExtendAngles(self, targetX, targetY, targetZ) -> list:
        try:
            D = math.sqrt(targetX**2 +targetY**2 +targetZ**2)
            linkLength = self.armLength
            #x = math.acos(D/(3*linkLength))
            #x,y,z = -x, 2*x, -2*x
            x = math.acos(math.sqrt(2*D/linkLength +3)/2 -0.5)
            x,y,z = (-x,3*x,-3*x)
        except:
            x,y,z = 0,0,0
        return (x,y,z)

    def setArmAngles(self, base, angle3, angle2, angle1):
        """Set the angles of the robotic arm segments"""
        self.reset()
        self.robot.rotate(x=0, y=base, z=0, centerAt=(132, -200, 0))
        self._rotateArm(self.arm3, angle3)
        self._rotateArm(self.arm2, angle2)
        self._rotateArm(self.arm1, angle1)

    def moveTo(self, targetX, targetY, targetZ):
        elevationAngle = self._getElevation(targetX, targetY)
        headingAngle   = self._getHeading(targetX, targetZ)
        x,y,z = self._getExtendAngles(targetX, targetY, targetZ)
#        print("X: %1.2f, Y: %1.2f"%(x,y))
        self.setArmAngles(headingAngle, elevationAngle +x, y, z)

    def tick(self, fps=30):
        """Update all elements"""
        self.time += 1/fps
