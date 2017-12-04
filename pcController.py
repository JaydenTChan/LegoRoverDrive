import ev3

def Main():
    ev3_1 = ev3.ev3("10.0.2.2", 5000)
    
    ev3_1.connect()
    
    while(ev3_1.conn == False):
        pass
    
    ev3_1.set_motor_speed("A", "50")
    
    input("Press Enter to continue...")
    
    ev3_1.disconnect()
    
    
 
if __name__ == '__main__':
    Main() 