import sys, serial, json

bt_ser = serial.Serial(
               port='/dev/ttyUSB1',
               baudrate = 38400,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=5
           )

# sends json data
def send_bt_data(data):
    bt_ser.write(str.encode(data))

# blocks until json command received, and returns stuff
def recv_bt_data():
    while True:
        response = {}
        try:
            json_command = bt_ser.readline().decode()
            response = json.loads(json_command)
        except:
            continue
        if response.get('command', '') is not '':
            return response

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        command = "AT+" + sys.argv[1] + "\r\n"
    else:
        command = "AT\r\n"

    bt_ser.write(command.encode())
    response = bt_ser.readline().decode()
    print(response)




