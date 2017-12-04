import socket
 
def Main():
    host = '127.0.0.1'
    port = 5000
     
    mySocket = socket.socket()
    mySocket.connect((host,port))

    mySocket.close()
 
if __name__ == '__main__':
    Main()