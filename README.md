## Setup

#### Hardware
connect bt


#### WIFI Connection Script
- `sudo ifconfig wlan0 up`
- `sudo iwlist wlan0 scan | grep ESSID` -> send this as json via bt
- wait for a response from BT with command wifi
- `wpa_passphrase <ssid> <password> | sudo tee wifi.conf`
- `sudo wpa_supplicant -c /etc/wpa_supplicant.conf -i wlan0` -> run in background and monitor this process
- `sudo dhclient wlan0` get ip address

SHOULD BE CONNECTED TO THE INTERNET NOW

#### Raspi Pinout
![pinout](files/pipinout.png)

#### State
periodically send the state to the BT controller


#### Server API

- `POST /device`
```json
{
    "status":"ok",
    "id": "<uid>" 
}
```

- `POST /device/:id/poke`
```json
{
    "status":"ok",
}
```
```json
{
    "status":"device not found"
}
```

- `GET /device/:id/poke` with timeout
```json
{
    "status":"ok",
    "poke": true
}
```
```json
{
    "status":"ok",
    "poke": false
}
```
```json
{
    "status":"device not found"
}
```

    