import ure as re
import picoweb

try:
    import network
except:
    pass

try:
    import usocket as socket
except:
    import socket

from machine import reset
from time import sleep
from json import dump, load

def settings(req, resp):
    # You can construct an HTTP response completely yourself, having
    # a full control of headers sent...
    yield from picoweb.start_response(resp, content_type = "text/html")
    htmlFile = open('www/config.html', 'r')
    for line in htmlFile:
        yield from resp.awrite(line)
    htmlFile.close()


def restart(req, resp):
    if req.method == "GET":
        yield from picoweb.start_response(resp)
    sleep(1)
    reset()


def config(req, resp):
    if req.method == "GET":
        yield from picoweb.start_response(resp, content_type = "application/json")
        jsonfile = open('config.json', 'r')
        for line in jsonfile:
            yield from resp.awrite(line)
        jsonfile.close()
    elif req.method == "POST":
        yield from req.read_form_data()
        storeConfig(req)
        yield from picoweb.start_response(resp, content_type = "text/html")
        htmlFile = open('www/config.html', 'r')
        for line in htmlFile:
            yield from resp.awrite(line)
        htmlFile.close()

    # Here's how you extract matched groups from a regex URI match


ROUTES = [
    # You can specify exact URI string matches...
    ("/settings", settings),
    ("/restart", restart),
    ("/config", config),
]


def storeConfig(req):
    jsonfile = open('config.json', 'r')
    j = load(jsonfile)
    jsonfile.close()

    j["WLAN"]["ssid"] = req.form["ssid"]
    j["WLAN"]["password"] = req.form["password"]
    j["OpenWeather"]["apikey"] = req.form["apikey"]
    j["OpenWeather"]["server"] = req.form["server"]
    j["OpenWeather"]["country"] = req.form["country"]
    j["OpenWeather"]["city"] = req.form["city"]
    j["OpenWeather"]["hemisphere"] = req.form["hemisphere"]
    j["OpenWeather"]["units"] = req.form["units"]
    j["ntp"]["server"] = req.form["ntp_server"]
    j["ntp"]["timezone"] = req.form["ntp_timezone"]
    j["schedule_power"]["on_time"] = req.form["on_time"]
    j["schedule_power"]["off_time"] = req.form["off_time"]

    jsonfile = open('config.json', 'w')
    dump(j, jsonfile)
    jsonfile.close()
    del j


def setupAP():
    ap = network.WLAN(network.AP_IF) # create access-point interface
    mac = list(ap.config('mac'))
    ssid = 'EPD47-{:0>2X}{:0>2X}{:0>2X}'.format(mac[3], mac[4], mac[5])
    ap.config(essid=ssid) # set the ESSID of the access point
    ap.config(max_clients=5) # set how many clients can connect to the network
    ap.active(True)         # activate the interface
    print("The hotspot has been established")
    print("please connect to the {} and output 192.168.4.1/settings in the browser to access the data page", ssid)


def setupWEB():
    setupAP()
    app = picoweb.WebApp(__name__, ROUTES)
    app.run(host="0.0.0.0", port=80, debug=1)
