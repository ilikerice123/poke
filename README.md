## Setup

#### Hardware
- Raspberry Pi Zero W
- Phone
- Wires and RGB LEDS

###
Essentially a remote controlled LED light that runs on a Raspberry PI. The Pi is identified with a uuid on the server, and it will send a GET request to the server that hangs forever until the phone app sends a similar post to the same uuid, in which case the GET request on the pi side will complete telling the Pi to flash its lights. The reason why it is a polling model (where the PI continually asks the server for an udpate), is because most routers block incoming TCP requests, which means the PI has to initiate the request.

This set up supports multiple LED pi poke devices connected to the same server, and new poke devices are registered and linked to a phone through a simple activation flow that I will update on the readme at some point. It works similar to how 2FA works with text messages. 

This was a Valentine's Day gift to my girlfriend, where she can put the device on her desk, and when I am thinking of her, I can send a poke from my phone, as long as the phone and the poke device are both connected to WIFI.

Here's a demo:

![demo](files/pokedemo.gif)

#### Setup [OUTDATED]
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