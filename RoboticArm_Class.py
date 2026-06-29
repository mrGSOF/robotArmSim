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
            filename="%s/RobotArm/base.stl"%folder, color=Colors.BLUE)\
            .rotate(-math.pi/2, 0, 0)\
            .translate(132, -200, 0)\
            .scale(0.3)\
            .setOrigin()
        armObj = Object(
            filename="%s/RobotArm/arm.stl"%folder, color=Colors.YELLOW)\
            .rotate(math.pi/2, 0, 0)\
            .scale(0.3)\
            .setCenter(scale=1.0, method="arithCenter")\
            .setOrigin()
        
        dot = Object(
            filename="%s/RobotArm/cube.json"%folder, color=Colors.RED)\
            .scale(3)\
            .translate(-132+135, 200, 0)\
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

        # arm.translate(-c[0], -c[1], -c[2])
        # arm.rotate(x=0, y=0, z=angle)
        # arm.translate(*c)

    def setArmAngles(self, base, angle3, angle2, angle1):
        """Set the angles of the robotic arm segments"""
        self.reset()
        self.robot.rotate(x=0, y=base, z=0, centerAt=(132, -200, 0))
        self._rotateArm(self.arm3, angle3)
        self._rotateArm(self.arm2, angle2)
        self._rotateArm(self.arm1, angle1)

    def moveTo(self, targetX, targetY, targetZ):
        D = math.sqrt(targetX**2 +targetY**2)
        linkLength = self.armLength
        elevationAngle = math.atan2(targetY, abs(targetX))
        headingAngle = math.atan2(targetX, targetZ)

        # 2cos(x)*armLength+cos(y)*armLength=D
        # 2sin(x)*armLength+sin(y)*armLength=0
        # self.setArmAngles(headingAngle+math.pi/2, (math.pi/2 -elevationAngle), 0,0)
        # return

        try:
            #print((3*linkLength**2+D**2)/(4*linkLength*D))
            x = math.acos((3*linkLength**2+D**2)/(4*linkLength*D))
            y = math.atan2(-2*math.sin(x), D/linkLength -2*math.cos(x))

            self.setArmAngles(headingAngle+math.pi/2, (math.pi/2 -elevationAngle)-x, -y,-x)
        except:
            self.setArmAngles(headingAngle+math.pi/2, (math.pi/2 -elevationAngle), 0,0)

    def tick(self, fps=60):
        """Update all elements"""
        self.time += 1/fps
