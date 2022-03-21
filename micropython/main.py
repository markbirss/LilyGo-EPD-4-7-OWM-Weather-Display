from json import load, loads
try:
    from time import localtime, ticks_ms, sleep
except:
    from time import localtime
try:
    import network
except:
    pass

try:
    from machine import deepsleep, ADC, Pin
except:
    pass

try:
    import usocket as socket
except:
    import socket

try:
    from framebuf1 import FrameBuffer
except:
    from framebuf import FrameBuffer

try:
    import urequests as requests
except ImportError:
    import requests

try:
    test = const(0)
except:
    def const(a):
        return a

wifi_signal = 0

SleepDuration = 60; # Sleep time in minutes, aligned to the nearest minute boundary, so if 30 will always update at 00 or 30 past the hour
WakeupHour    = 8;  # Don't wakeup until after 07:00 to save battery power
SleepHour     = 23; # Sleep after 23:00 to save battery power
CurrentHour = 0
CurrentMin = 0
CurrentSec = 0
Delta = 30
weather = None
forcast = None

max_readings = const(24)
Language = "EN"

f = open("config.json", "r")
config = load(f)

ssid = config["WLAN"]["ssid"]
password = config["WLAN"]["password"]

apikey     = config["OpenWeather"]["apikey"]
server     = config["OpenWeather"]["server"]
Country    = config["OpenWeather"]["country"]
City       = config["OpenWeather"]["city"]
Hemisphere = config["OpenWeather"]["hemisphere"]
Units      = config["OpenWeather"]["units"]

ntpServer = config["ntp"]["server"]
Timezone = config["ntp"]["timezone"]

def StartWiFi():
    global wifi_signal
    print("\r\nConnecting to: {}".format(ssid))
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(reconnects=3)
    for _ in range(0, 3):
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            sleep(1)
    if wlan.isconnected():
        wifi_signal = wlan.status('rssi')
    print('network config:', wlan.ifconfig())
    return wlan.status()

def obtainWeatherData(request):
    units = "metric" if Units == "M" else "imperial"

    uri = '/data/2.5/{}?q={},{}&APPID={}&mode=json&units={}&lang={}'.format(
        request, City, Country, apikey, units, Language)
    if request != "weather":
        uri = '{}&cnt={}'.format(uri, str(max_readings))

    print("request uri: %s"%(uri))

    r = requests.get("http://{}{}".format(server, uri))
    DecodeWeather(request, r.json())
    r.close()
    if request == "weather" and weather is None:
        return False
    elif request == "forcast" and forcast is None:
        return False 
    return True
    #s = socket.socket()

    #ai = socket.getaddrinfo(server, 80)
    #print("Address infos:", ai)
    #addr = ai[0][-1]

    #print("Connect address:", addr)
    #s.connect(addr)

    #if use_stream:
        # MicroPython socket objects support stream (aka file) interface
        # directly, but the line below is needed for CPython.
        #s = s.makefile("rwb", 0)
        #s.send(bytearray("GET {} HTTP/1.0\r\n\r\n".format(url)))
        #print(s.read())
    #else:
    #s.send(bytearray("GET {} HTTP/1.0\r\n\r\n".format(uri)))
    #while True:
    #data = s.readline()
    #    if len(data) == 0:
    #        print("close socket")
    #        break
    #    print(data)
    #s.close()
    #DecodeWeather(request, "")

def DecodeWeather(request, data):
    if request == "weather":
        global CurrentMin
        global CurrentSec
        tm = localtime(data["dt"] + data["timezone"])
        CurrentMin = tm[4]
        CurrentSec = tm[5]
        global weather
        weather = data
    elif request == "forecast":
        global forcast
        forcast = data

def BeginSleep():
    # Some ESP32 have a RTC that is too fast to maintain accurate time, so add an offset
    SleepTimer = int((SleepDuration * 60 - ((CurrentMin % SleepDuration) * 60 + CurrentSec)) + Delta)
    print("Awake for : {:.3f}-secs".format(round(ticks_ms() / 1000.0, 3)))
    print("Entering {:d} (secs) of sleep time".format(SleepTimer))
    print("Starting deep-sleep period...")
    deepsleep(SleepTimer * 1000)


if __name__ == "__main__":
    from ui import InitUI, DisplayWeather
    import gc
    adc = ADC(Pin(36))

    gc.enable()
    buffer = [ 0 for i in range(0, int(960 * 540 / 2)) ]
    fb = FrameBuffer(buffer, 960, 540)
    fb.fill(255)
    InitUI(fb)

    #if StartWiFi() == network.STAT_GOT_IP  and SetupTime() == True:
    if StartWiFi() == network.STAT_GOT_IP:
        WakeUp = False
        Attempts = 1
        RxWeather = False
        RxForecast = False
        while (RxWeather == False or RxForecast == False) and Attempts <= 2:
            # Try up-to 2 time for Weather and Forecast data
            if RxWeather == False:
                RxWeather = obtainWeatherData("weather")
            #if RxWeather == True:
            #    if WakeupHour > SleepHour:
            #        WakeUp = CurrentHour >= WakeupHour or CurrentHour <= SleepHour
            #    else:
            #        WakeUp = CurrentHour >= WakeupHour and CurrentHour <= SleepHour
            #    if WakeUp == False:
            #        BeginSleep()
            if RxForecast == False:
                RxForecast = obtainWeatherData("forecast")
            Attempts += 1
        print("Received all weather data...")
            
        if RxWeather and RxForecast:
            DisplayWeather(weather, forcast, wifi_signal, adc.read()/4096.0 * 5)
            try:
                from epd import EPD47
                e = EPD47()
                e.power(True)
                e.clear()
                e.bitmap(buffer, 0, 0, 960, 540)
                e.power(False)
                del e
            except:
                print("The current parser is not micropython")
    BeginSleep()

