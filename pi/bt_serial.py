import sys, serial, json
import bluetooth
import subprocess

subprocess.run(['sudo', 'hciconfig', 'hci0', 'piscan'])

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