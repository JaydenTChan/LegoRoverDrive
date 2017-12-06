import ev3
import time
import obj_detection as obj
import numpy as np
import cv2 
from matplotlib import pyplot as plt
import imutils



def Main():
    ev3_1 = ev3.ev3("10.0.2.5", 5000) #laura (steering)
    ev3_2 = ev3.ev3("10.0.2.1", 5001) #cthulu (speed)
    
    ev3_1.connect()
    ev3_2.connect()

    """
    ev3_2.set_motor_speed("A", "50")
    ev3_2.set_angle("B", "50", "90")
    """
    

    turnRightDiag(ev3_1)
    time.sleep(1)
    forward(ev3_2, "0")
    time.sleep(5)
    turnLeftDiag(ev3_1)

    
    input("Press Enter to continue...")
    
    ev3_1.disconnect()
    ev3_2.disconnect()
    
    

def moveGrid(ev3_1, ev3_2, pos, target):

    pass
    
def forward(ev3, angle):
    ev3.set_angle("A", "50", "1440")
    ev3.set_angle("B", "50", "1440")
    ev3.set_angle("C", "50", "1440")
    
def stop(ev3):
    ev3.set_angle("A", "0")
    ev3.set_angle("B", "0")
    ev3.set_angle("C", "0")

def turnRight(ev3):
    """
    Use with Laura ev3
    """
    ev3.set_angle("A", "30", "90")
    ev3.set_angle("B", "-30", "-90")
    ev3.set_angle("C", "30", "90")

def turnLeft(ev3):
    """
    Use with Laura ev3
    """
    ev3.set_angle("A", "-30", "-90")
    ev3.set_angle("B", "30", "90")
    ev3.set_angle("C", "-30", "-90")

def turnRightDiag(ev3):
    """
    Use with Laura ev3
    """
    ev3.set_angle("A", "30", "45")
    ev3.set_angle("B", "-30", "-45")
    ev3.set_angle("C", "30", "45")

def turnLeftDiag(ev3):
    """
    Use with Laura ev3
    """
    ev3.set_angle("A", "-30", "-45")
    ev3.set_angle("B", "30", "45")
    ev3.set_angle("C", "-30", "-45")
    

    
if __name__ == '__main__':
    Main() 