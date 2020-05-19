import sys, serial, json
import bluetooth

# bt_ser = serial.Serial(
#                port='/dev/ttyUSB0',
#                baudrate = 38400,
#                parity=serial.PARITY_NONE,
#                stopbits=serial.STOPBITS_ONE,
#                bytesize=serial.EIGHTBITS,
#                timeout=5
#            )

# # sends json data
# def send_bt_data(data):
#     bt_ser.write(str.encode(data))

# # blocks until json command received, and returns stuff
# def recv_bt_data():
#     while True:
#         response = {}
#         try:
#             json_command = bt_ser.readline().decode()
#             response = json.loads(json_command)
#         except:
#             continue
#         if response.get('command', '') is not '':
#             return response

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



