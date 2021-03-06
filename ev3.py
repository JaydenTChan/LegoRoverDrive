import socket
import time

class ev3:
    """
    A Python class made to represent an EV3
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.conn = False
        
    def connect(self):
        """
        Use this function to connect to the EV3
        """
        try:
            self.socket.connect((self.ip,self.port))
            self.conn = True
        except Exception as e:
            print("Error connecting to EV3!")
            
    def disconnect(self):
        """
        Use this when disconnecting EV3
        """
        if self.conn != False:
            self.send_data("2")
            self.socket.close()
        else:
            print("Connection Not Yet Made!")
            
    def send_data(self, message):
        """
        This function sends a message to the EV3 in question
        
        Action Codes:
        1. Set motor speed
        
        :param message: The message to be sent
        """
        if self.conn != False:
            try:
                message = message + '\n'
                self.socket.sendall(message.encode('UTF-8'))
            except Exception:
                print("Error sending command!")
        else:
            print("Connection not yet made!")
            
    def receive_data(self):
        """
        Use this function to read from the socket
        """
        if self.conn != False:
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except Exception:
                print("Error receiving messages!")
            return data
        else:
            print("Connection not yet made!")
            return None
            
    def set_motor_speed(self, motor, speed):
        """
        This function will set speed of an EV3 motor
        
        :param motor: Which motor (A/B/C/D)
        :param speed: Speed to run the motor 0-100
        """
        if self.conn != False:
            self.send_data("1")
            self.send_data(motor)
            self.send_data(speed)
        else:
            print("Connection not yet made!")
    
    def set_angle(self, motor, speed, angle):
        """
        This function will set anngle of an EV3 motor
        
        :param motor: Which motor (A/B/C/D)
        :param speed: Speed to run the motor 0-100
        """
        if self.conn != False:
            self.send_data("3")
            self.send_data(motor)
            self.send_data(speed)
            self.send_data(angle)
        else:
            print("Connection not yet made!")
        
    def forward(self, angle):
        angle = str(angle)
        self.set_angle("A", "50", angle)
        self.set_angle("B", "50", angle)
        self.set_angle("C", "50", angle)
        
    def stop(self):
        self.set_angle("A", "0", "0")
        self.set_angle("B", "0", "0")
        self.set_angle("C", "0", "0")

    def turnRight(self):
        """
        Use with Laura ev3
        """
        self.set_angle("A", "30", "90")
        self.set_angle("B", "-30", "-90")
        self.set_angle("C", "30", "90")

    def turnLeft(self):
        """
        Use with Laura ev3
        """
        self.set_angle("A", "-30", "-90")
        self.set_angle("B", "30", "90")
        self.set_angle("C", "-30", "-90")

    def turnRightDiag(self):
        """
        Use with Laura ev3
        """
        self.set_angle("A", "30", "45")
        self.set_angle("B", "-30", "-45")
        self.set_angle("C", "30", "45")

    def turnLeftDiag(self):
        """
        Use with Laura ev3
        """
        self.set_angle("A", "-30", "-45")
        self.set_angle("B", "30", "45")
        self.set_angle("C", "-30", "-45")