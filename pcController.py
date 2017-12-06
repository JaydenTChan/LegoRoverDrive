import ev3
import time

def Main():
    ev3_1 = ev3.ev3("10.0.2.5", 5000) #laura (steering)
    ev3_2 = ev3.ev3("10.0.2.1", 5001) #chuthulu (speed)
    
    ev3_1.connect()
    ev3_2.connect()

    """
    ev3_2.set_motor_speed("A", "50")
    ev3_2.set_angle("B", "50", "90")
    """
    
    turnleft(ev3_1)
    time.sleep(1)
    forward(ev3_2)
    
    input("Press Enter to continue...")
    
    ev3_1.disconnect()
    ev3_2.disconnect()
    
    

def movegrid(ev3_1, ev3_2, pos, target):

    pass
    
def forward(ev3):
    ev3.set_motor_speed("A", "30")
    ev3.set_motor_speed("B", "30")
    ev3.set_motor_speed("C", "30")
    
def stop(ev3):
    ev3.set_motor_speed("A", "0")
    ev3.set_motor_speed("B", "0")
    ev3.set_motor_speed("C", "0")

def turnright(ev3):
    ev3.set_angle("A", "30", "90")
    ev3.set_angle("B", "30", "90")
    ev3.set_angle("C", "30", "90")

def turnleft(ev3):
    ev3.set_angle("A", "-30", "-90")
    ev3.set_angle("B", "-30", "-90")
    ev3.set_angle("C", "-30", "-90")

    

    
if __name__ == '__main__':
    Main() 