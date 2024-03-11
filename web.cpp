#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <esp_heap_caps.h>
#include <ArduinoJson.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include "FS.h"
#include "SPIFFS.h"

static WebServer server(80);

void storeConfig();

void handleRoot()
{
    server.send(200, "text/plain", "hello from esp32!");
}


void handleSettings()
{
    File file = SPIFFS.open("/config.html", "r");
    if (!file)
    {
        Serial.println("file error");
    }
    server.streamFile(file, "text/html");
    file.close();
}


void handleConfig()
{
    storeConfig();

    // server.send(302, "text/html");
    File htmlfile = SPIFFS.open("/config.html", "r");
    if (!htmlfile)
    {
        Serial.println("file error");
    }
    server.streamFile(htmlfile, "text/html");
    htmlfile.close();
}


void handleNotFound()
{
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET) ? "GET" : "POST";
    message += "\nArguments: ";
    message += server.args();
    message += "\n";
    for (uint8_t i = 0; i < server.args(); i++)
    {
        message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
    }
    server.send(404, "text/plain", message);
}


void setupAP()
{
    Serial.println("Configuring access point...");
    uint8_t mac[6];
    char buff[128];
    WiFi.macAddress(mac);
    sprintf(buff, "T-EPD47-%02X%02X", mac[4], mac[5]);
    WiFi.softAP(buff);
    Serial.printf("The hotspot has been established");
    Serial.printf("please connect to the %s and output 192.168.4.1/settings in the browser to access the data page \n", buff);
}


void webTask(void *args)
{
    while (1)
    {
        server.handleClient();
        delay(10); //allow the cpu to switch to other tasks
    }
    vTaskDelete(NULL);
}


void setupWEB(void)
{
    Serial.begin(115200);
    setupAP();

    server.on("/", handleRoot);
    server.on("/settings", handleSettings);
    server.on("/config", HTTP_POST, handleConfig);
    server.on("/config", HTTP_GET, []() {
        File file = SPIFFS.open("/config.json", "r");
        size_t sent = server.streamFile(file, "application/json");
        file.close();
        return;
    });
    server.on("/restart", HTTP_GET, []() {
        server.send(200);
        delay(1000);
        ESP.restart();
        return;
    });

    server.onNotFound(handleNotFound);

    server.begin();
    Serial.println("HTTP server started");

    TaskHandle_t t1;
    xTaskCreatePinnedToCore((void (*)(void *))webTask, "webTask", 8192, NULL, 10, &t1, 0);
}


void storeConfig()
{
    StaticJsonDocument<1024> doc;

    File configfile = SPIFFS.open("/config.json", "r");
    DeserializationError error = deserializeJson(doc, configfile);
    if (error)
        Serial.println(F("Failed to read file, using default configuration"));
    configfile.close();

    for ( uint8_t i = 0; i < server.args(); i++ )
    {
        if (server.argName(i).equals("ssid"))
        {
            doc["WLAN"]["ssid"] = server.arg(i);
        }
        else if (server.argName(i).equals("password"))
        {
            doc["WLAN"]["password"] = server.arg(i);
        }
        else if (server.argName(i).equals("apikey"))
        {
            doc["OpenWeather"]["apikey"] = server.arg(i);
        }
        else if (server.argName(i).equals("server"))
        {
            doc["OpenWeather"]["server"] = server.arg(i);
        }
        else if (server.argName(i).equals("country"))
        {
            doc["OpenWeather"]["country"] = server.arg(i);
        }
        else if (server.argName(i).equals("city"))
        {
            doc["OpenWeather"]["city"] = server.arg(i);
        }
        else if (server.argName(i).equals("hemisphere"))
        {
            doc["OpenWeather"]["hemisphere"] = server.arg(i);
        }
        else if (server.argName(i).equals("units"))
        {
            doc["OpenWeather"]["units"] = server.arg(i);
        }
        else if (server.argName(i).equals("ntp_server"))
        {
            doc["ntp"]["server"] = server.arg(i);
        }
        else if (server.argName(i).equals("ntp_timezone"))
        {
            doc["ntp"]["timezone"] = server.arg(i);
        }
        else if (server.argName(i).equals("on_time"))
        {
            doc["schedule_power"]["on_time"] = server.arg(i);
        }
        else if (server.argName(i).equals("off_time"))
        {
            doc["schedule_power"]["off_time"] = server.arg(i);
        }
    }

    configfile = SPIFFS.open("/config.json", FILE_WRITE);
    if (!configfile)
    {
        Serial.println("file error");
    }
    if (serializeJson(doc, configfile) == 0)
    {
        Serial.println(F("Failed to write to file"));
    }
    configfile.close();
}