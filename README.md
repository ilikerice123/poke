## Setup

#### Hardware
Raspberry Pi Zero W
Phone

#### Setup
install pigpio to root
`sudo apt install python3-pip`
import python libraries
make `server.txt` file
install android sdk, accept licenses
install java 8 sdk (a huge pain)
change gradle settings to build


## files/
used to store random files

## pi/
Raspi Pinout (PI GPIO uses broadcom (BCM) pin notation)

![pinout](files/pipinout.png)

- `check_wifi.sh` script that echos ok or error based on whether it can ping google.com (connection test)
- `pigpio.sh` runs pi-gpio daemon for generation of pwm signals
- `wpa_script.sh` generates wpa file, and attempts to connect to WPA enabled router
- `bt_serial.py` provides interface with serial bt device
- `api.py` provides interface with server
- `leds.py` provides interface to leds
- `logic.py` main file that runs the state machine logic
- `state.py` stores class for state
- `wifi_script.py` provides interface to connect to internet

## server/

Server API:
- `POST /device`
```json
{
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
    "poke": true
}
```
```json
{
    "poke": false
}
```
```json
{
    "status":"device not found"
}
```

- `POST /device/:code/activate`
```json
{
    "id": "<uuid>"
}
```
```json
{
    "status": "device not found"
}
```

- `GET /device/:code/activate`
```json
{
    "id": "<uuid>",
    "activated": "<true/false>"
}
```
hangs until activated

#### TODO:
- remove unnecessary prints in pi script
- fix returning 200 when device is not found