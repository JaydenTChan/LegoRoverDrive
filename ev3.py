import socket

"""
    host = "127.0.0.1"
    port = 7777
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
                break
        print ("from connected  user: " + str(data))
         
        data = str(data).upper()
        print ("sending: " + str(data))
        conn.send(data.encode())
             
    conn.close()
     
"""


class ev3:
    """
    A Python class made to represent an EV3
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.conn = None
        self.addr = None
        
    def connect(self):
        """
        Use this function to connect to the EV3
        """
        try:
            self.socket.bind((self.ip,self.port))
            self.socket.listen(1)
            self.conn, self.addr = self.socket.accept()
        except Exception as e:
            print("Error connecting to EV3!")
            
    def disconnect(self):
        """
        Use this when disconnecting EV3
        """
        if self.conn != None:
            self.conn.close()
        else:
            print("Connection Not Yet Made!")
            
    def send_data(self, message):
        """
        This function sends a message to the EV3 in question
        
        Action Codes:
        1. Set motor speed
        
        :param message: The message to be sent
        """
        if self.conn != None:
            try:
                self.conn.send(message.encode())
            except Exception:
                print("Error sending command!")
        else:
            print("Connection not yet made!")
            
    def receive_data(self):
        """
        Use this function to read from the socket
        """
        if self.conn != None:
            try:
                data = self.conn.recv(1024).decode()
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
        if self.conn != None:
            send_data("1")
            send_data(motor)
            send_data(speed)
        else:
            print("Connection not yet made!")
        
        