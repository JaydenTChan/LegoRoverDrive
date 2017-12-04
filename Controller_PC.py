import socket

from ev3
 
def Main():
    #ev3_1 = ev3("10.0.2.1", "7777")
    #ev3_2 = ev3("10.0.2.2", "7778")
    
    #ev3_1.connect()
    #ev3_2.connect()
    
    host = "127.0.0.1"
    port = 1111
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(5)
    
    print("Waiting for connection")
    conn, addr = mySocket.accept()
    
    print("Connection accepted")
    
    conn.close()
    

if __name__ == '__main__':
    Main()