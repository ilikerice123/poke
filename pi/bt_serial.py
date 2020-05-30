import sys, json
import bluetooth
import subprocess

client_sock = None
subprocess.run(['sudo', 'hciconfig', 'hci0', 'piscan'])
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_sock.bind(("",1))
server_sock.listen(1)

def init_socket():
    global client_sock
    if(client_sock is None):
        client_sock,address = server_sock.accept()
        print("Accepted connection from " + str(address))

def send(json):
    global client_sock
    try:
        init_socket()
        client_sock.send(json.encode())
    except:
        client_sock.close()
        client_sock = None

def recv():
    global client_sock
    try:
        init_socket()
        data = client_sock.recv(1024)
        return data.decode()
    except:
        client_sock.close()
        client_sock = None
        return None

if __name__ == '__main__':
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
    
    client_sock,address = server_sock.accept()
    print("Accepted connection from " + str(address))
    
    data = client_sock.recv(1024)
    print("received [%s]" % data)
    
    client_sock.close()
    server_sock.close()