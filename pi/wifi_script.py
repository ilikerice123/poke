import subprocess, json
import bt_serial as bluetooth

WPA_FILE = 'wifi.conf'

def connect():
    proc = subprocess.Popen(['sudo', 'ifconfig', 'wlan0', 'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = proc.wait()
    if(err != 0):
        print('error bringing wlan up!')
        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
        return False
        #try again

    # continuously request wifi info from phone
    response = {}
    while(response.get('command', '') != 'wifi'):
        scan_proc = subprocess.Popen(['sudo', 'iwlist', 'wlan0', 'scanning'], stdout=subprocess.PIPE)
        grep_proc = subprocess.Popen(['grep', 'ESSID'], stdin=scan_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = scan_proc.wait()
        scan_proc.stdout.close()
        stdout, stderr = grep_proc.communicate()
        if(err != 0):
            print('error scanning!')
            return False
        request = json.dumps({'command': 'wifi_list', 'ssids': [ssid.strip() for ssid in stdout.decode().split("\n")]})
        print(request)
        bluetooth.send_bt_data(request)
        print('waiting for response from bt')
        response = bluetooth.recv_bt_data()
    
    proc1 = subprocess.Popen(['wpa_passphrase', response['ssid'], response['password']], stdout=subprocess.PIPE)
    subprocess.Popen(['sudo', 'tee', WPA_FILE], stdin=proc1.stdout)
    err = proc1.wait()
    proc1.stdout.close()

    proc = subprocess.Popen(['sudo', './wpa_script.sh', WPA_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = proc.wait()
    if(err != 0):
        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
        return False

    completed_proc = subprocess.run(['sudo', 'dhclient', 'wlan0'])
    if(completed_proc.returncode == 0):
        return True

def has_wifi():
    proc = subprocess.run(['./check_wifi.sh'], stdout=subprocess.PIPE)
    return proc.stdout == 'ok'

if __name__ == "__main__":
    connect()
