
from math import floor, cos, sin, pi, sqrt
from time import localtime
try:
    from example.weather.lang import *
except:
    from lang import *

try:
    from example.weather.FiraSansRegular8pt import FiraSansRegular8pt
except:
    from FiraSansRegular8pt import FiraSansRegular8pt

try:
    from example.weather.FiraSansRegular10pt import FiraSansRegular10pt
except:
    from FiraSansRegular10pt import FiraSansRegular10pt

try:
    from example.weather.FiraSansRegular12pt import FiraSansRegular12pt
except:
    from FiraSansRegular12pt import FiraSansRegular12pt

try:
    from example.weather.FiraSansRegular18pt import FiraSansRegular18pt
except:
    from FiraSansRegular18pt import FiraSansRegular18pt

try:
    from example.weather.FiraSansRegular24pt import FiraSansRegular24pt
except:
    from FiraSansRegular24pt import FiraSansRegular24pt

try:
    test = const(0)
except:
    def const(a):
        return a

White = const(0xFF)
LightGrey = const(0xBB)
Grey = const(0x88)
DarkGrey = const(0x44)
Black = const(0x00)

LEFT = const(0)
RIGHT = const(1)
CENTER = const(2)

LargeIcon = True
SmallIcon = False

Large = const(20)  # For icon drawing
Small = const(8)  # For icon drawing

framebuf = None
currentFont = FiraSansRegular8pt

SCREEN_WIDTH = const(960)
SCREEN_HEIGHT = const(540)


def InitUI(fb):
    global framebuf
    framebuf = fb


def DisplayStatusSection(x, y, rssi, voltage):
    setFont(FiraSansRegular8pt)
    DrawRSSI(x + 305, y + 15, rssi)
    DrawBattery(x + 150, y, voltage)


def DisplayGeneralInfoSection(weather):
    setFont(FiraSansRegular10pt)
    drawString(5, 2, weather["name"], LEFT)
    setFont(FiraSansRegular8pt)
    now_utc = localtime(weather["dt"] + weather["timezone"])
    print(now_utc)
    try:
        drawString(500, 2, "{:s}, {:0>2d} {:s} {:0>4d}  @   {:0>2d}:{:0>2d}:{:0>2d}".format(
                    weekday_D[now_utc.tm_wday], now_utc.tm_mday, now_utc.tm_mon,
                    now_utc.tm_year, now_utc.tm_hour, now_utc.tm_min,
                    now_utc.tm_sec), LEFT)
    except:
        drawString(500, 2, "{:s}, {:0>2d} {:s} {:0>4d}  @   {:0>2d}:{:0>2d}:{:0>2d}".format(
                    weekday_D[now_utc[6]], now_utc[2], month_M[now_utc[1]],
                    now_utc[0] - 30, now_utc[3], now_utc[4], now_utc[5]), LEFT)


def DisplayDisplayWindSection(x, y, angle, windspeed, Cradius, units):
    # Show wind direction on outer circle of width and length
    arrow(x, y, Cradius - 22, angle, 18, 33)
    setFont(FiraSansRegular8pt)
    dxo = 0
    dyo = 0
    dxi = 0
    dyi = 0
    framebuf.circle(x, y, Cradius, Black)       # Draw compass circle
    framebuf.circle(x, y, Cradius + 1, Black)   # Draw compass circle
    framebuf.circle(x, y, Cradius * 0.7, Black)  # Draw compass inner circle
    # for a in range(0, 360, 22.5):
    a = 0.0
    while a < 360:
        dxo = Cradius * cos((a - 90) * pi / 180)
        dyo = Cradius * sin((a - 90) * pi / 180)
        if int(a) == 45:
            drawString(dxo + x + 15, dyo + y - 18, TXT_NE, CENTER)
        if int(a) == 135:
            drawString(dxo + x + 20, dyo + y - 2, TXT_SE, CENTER)
        if int(a) == 225:
            drawString(dxo + x - 20, dyo + y - 2, TXT_SW, CENTER)
        if int(a) == 315:
            drawString(dxo + x - 15, dyo + y - 18, TXT_NW, CENTER)
        dxi = dxo * 0.9
        dyi = dyo * 0.9
        framebuf.line(dxo + x, dyo + y, dxi + x, dyi + y, Black)
        dxo = dxo * 0.7
        dyo = dyo * 0.7
        dxi = dxo * 0.9
        dyi = dyo * 0.9
        framebuf.line(dxo + x, dyo + y, dxi + x, dyi + y, Black)
        a += 22.5
    drawString(x, y - Cradius - 20, TXT_N, CENTER)
    drawString(x, y + Cradius + 10, TXT_S, CENTER)
    drawString(x - Cradius - 15, y - 5, TXT_W, CENTER)
    drawString(x + Cradius + 10, y - 5, TXT_E, CENTER)
    drawString(x + 3, y + 50, "{:.0f}°".format(angle), CENTER)
    setFont(FiraSansRegular12pt)
    drawString(x, y - 50, WindDegToOrdinalDirection(angle), CENTER)
    setFont(FiraSansRegular24pt)
    drawString(x + 3, y - 18, "{:.1f}".format(windspeed), CENTER)
    setFont(FiraSansRegular12pt)
    drawString(x, y + 25, "m/s" if units == "M" else "mph", CENTER)


def WindDegToOrdinalDirection(winddirection):
    if (winddirection >= 348.75 or winddirection < 11.25):
        return TXT_N
    if (winddirection >= 11.25 and winddirection < 33.75):
        return TXT_NNE
    if (winddirection >= 33.75 and winddirection < 56.25):
        return TXT_NE
    if (winddirection >= 56.25 and winddirection < 78.75):
        return TXT_ENE
    if (winddirection >= 78.75 and winddirection < 101.25):
        return TXT_E
    if (winddirection >= 101.25 and winddirection < 123.75):
        return TXT_ESE
    if (winddirection >= 123.75 and winddirection < 146.25):
        return TXT_SE
    if (winddirection >= 146.25 and winddirection < 168.75):
        return TXT_SSE
    if (winddirection >= 168.75 and winddirection < 191.25):
        return TXT_S
    if (winddirection >= 191.25 and winddirection < 213.75):
        return TXT_SSW
    if (winddirection >= 213.75 and winddirection < 236.25):
        return TXT_SW
    if (winddirection >= 236.25 and winddirection < 258.75):
        return TXT_WSW
    if (winddirection >= 258.75 and winddirection < 281.25):
        return TXT_W
    if (winddirection >= 281.25 and winddirection < 303.75):
        return TXT_WNW
    if (winddirection >= 303.75 and winddirection < 326.25):
        return TXT_NW
    if (winddirection >= 326.25 and winddirection < 348.75):
        return TXT_NNW
    return "?"


def DisplayAstronomySection(x, y, weather):
    setFont(FiraSansRegular10pt)
    drawString(x + 5, y + 30, '{} {}'.format(
        ConvertUnixTime(weather["sys"]["sunrise"])[0:5], TXT_SUNRISE), LEFT)
    drawString(x + 5, y + 50, '{} {}'.format(
        ConvertUnixTime(weather["sys"]["sunset"])[0:5], TXT_SUNSET), LEFT)

    now_utc = localtime()
    try:
        drawString(x + 5, y + 70, MoonPhase(now_utc.tm_mday,
                   now_utc.tm_mon, now_utc.tm_year, Hemisphere), LEFT)
    except:
        drawString(x + 5, y + 70, MoonPhase(now_utc[2],
                   now_utc[1], now_utc[0], Hemisphere), LEFT)
    DrawMoon(x + 160, y - 15, now_utc[2], now_utc[1], now_utc[0], Hemisphere)


def JulianDate(d, m, y):
    mm = yy = k1 = k2 = k3 = j = 0
    yy = y - floor((12 - m) / 10)
    mm = m + 9
    if (mm >= 12):
        mm = mm - 12
    k1 = floor(365.25 * (yy + 4712))
    k2 = floor(30.6001 * mm + 0.5)
    k3 = floor(floor((yy / 100) + 49) * 0.75) - 38
    j = k1 + k2 + d + 59 + 1
    if (j > 2299160):
        j = j - k3
    return j


def NormalizedMoonPhase(d, m, y):
    j = JulianDate(d, m, y)
    # Calculate approximate moon phase
    Phase = (j + 4.867) / 29.53059
    return Phase - Phase


def DrawMoon(x, y, dd, mm, yy, hemisphere):
    diameter = 75
    Phase = NormalizedMoonPhase(dd, mm, yy)
    hemisphere.lower()
    if hemisphere == "south":
        Phase = 1 - Phase
    # Draw dark part of moon
    framebuf.fill_circle(x + diameter - 1, y + diameter, diameter / 2 + 1, LightGrey)
    number_of_lines = 90
    for Ypos in range(0, floor(number_of_lines / 2) + 1):
        Xpos = sqrt(number_of_lines / 2 * number_of_lines / 2 - Ypos * Ypos)
        # Determine the edges of the lighted part of the moon
        Rpos = 2 * Xpos
        Xpos1 = 0
        Xpos2 = 0
        if Phase < 0.5:
            Xpos1 = -Xpos
            Xpos2 = Rpos - 2 * Phase * Rpos - Xpos
        else:
            Xpos1 = Xpos
            Xpos2 = Xpos - 2 * Phase * Rpos + Rpos
        # Draw light part of moon
        pW1x = (Xpos1 + number_of_lines) / number_of_lines * diameter + x
        pW1y = (number_of_lines - Ypos) / number_of_lines * diameter + y
        pW2x = (Xpos2 + number_of_lines) / number_of_lines * diameter + x
        pW2y = (number_of_lines - Ypos) / number_of_lines * diameter + y
        pW3x = (Xpos1 + number_of_lines) / number_of_lines * diameter + x
        pW3y = (Ypos + number_of_lines) / number_of_lines * diameter + y
        pW4x = (Xpos2 + number_of_lines) / number_of_lines * diameter + x
        pW4y = (Ypos + number_of_lines) / number_of_lines * diameter + y
        framebuf.line(pW1x, pW1y, pW2x, pW2y, White)
        framebuf.line(pW3x, pW3y, pW4x, pW4y, White)
    framebuf.circle(x + diameter - 1, y + diameter, diameter / 2, Black)


def MoonPhase(d, m, y, hemisphere):
    c = 0
    e = 0
    jd = 0.0
    b = 0
    if m < 3:
        y -= 1
        m += 12
    m += 1
    c = 365.25 * y
    e = 30.6 * m
    jd = c + e + d - 694039.09  # jd is total days elapsed */
    jd /= 29.53059             # divide by the moon cycle (29.53 days) */
    b = jd                     # int(jd) -> b, take integer part of jd */
    jd -= b                    # subtract integer part to leave fractional part of original jd */
    b = jd * 8 + 0.5           # scale fraction from 0-8 and round by adding 0.5 */
    # 0 and 8 are the same phase so modulo 8 for 0 */
    b = int(b) & 7
    if hemisphere == "south":
        b = 7 - b
    if b == 0:
        return TXT_MOON_NEW  # New;              0%  illuminated
    if b == 1:
        return TXT_MOON_WAXING_CRESCENT  # Waxing crescent; 25%  illuminated
    if b == 2:
        return TXT_MOON_FIRST_QUARTER  # First quarter;   50%  illuminated
    if b == 3:
        return TXT_MOON_WAXING_GIBBOUS  # Waxing gibbous;  75%  illuminated
    if b == 4:
        return TXT_MOON_FULL  # Full;            100% illuminated
    if b == 5:
        return TXT_MOON_WANING_GIBBOUS  # Waning gibbous;  75%  illuminated
    if b == 6:
        return TXT_MOON_THIRD_QUARTER  # Third quarter;   50%  illuminated
    if b == 7:
        return TXT_MOON_WANING_CRESCENT  # Waning crescent; 25%  illuminated
    return ""


def DisplayMainWeatherSection(x, y, weather, forcast):
    setFont(FiraSansRegular8pt)
    DisplayTemperatureSection(x, y - 40, weather)
    DisplayForecastTextSection(x - 55, y + 25, weather, forcast)
    DisplayPressureSection(x - 25, y + 90, weather, forcast)


def DisplayWeatherIcon(x, y, weather):
    DisplayConditionsSection(x, y, weather["weather"][0]["icon"], LargeIcon)


def DisplayForecastSection(x, y, forcast):
    WxForecast = forcast['list']
    pressure_readings = []
    temperature_readings = []
    humidity_readings = []
    rain_readings = []
    snow_readings = []
    for i in range(0, max_readings):
        DisplayForecastWeather(x, y, i, forcast)

    for r in range(0, max_readings):
        ''' Pre-load temporary arrays with with data - because C parses by
        reference and remember that[1] has already been converted to I units
        '''
        if (Units == "I"):
            pressure_readings.append(WxForecast[r]["main"]["pressure"] * 0.02953)
        else:
            pressure_readings.append(WxForecast[r]["main"]["pressure"])
        if (Units == "I"):
            try:
                rain_readings.append(WxForecast[r]["rain"]["3h"] * 0.0393701)
            except:
                rain_readings.append(0.0 * 0.0393701)
        else:
            try:
                rain_readings.append(WxForecast[r]["rain"]["3h"])
            except:
                rain_readings.append(0.0)
        if (Units == "I"):
            try:
                snow_readings.append(WxForecast[r]["snow"]["3h"] * 0.0393701)
            except:
                snow_readings.append(0.0 * 0.0393701)
        else:
            try:
                snow_readings.append(WxForecast[r]["snow"]["3h"])
            except:
                snow_readings.append(0.0)
        temperature_readings.append(WxForecast[r]["main"]["temp"])
        humidity_readings.append(WxForecast[r]["main"]["humidity"])

    gwidth = 175
    gheight = 100
    gx = (SCREEN_WIDTH - gwidth * 4) / 5 + 8
    gy = (SCREEN_HEIGHT - gheight - 30)
    gap = gwidth + gx
    # (x,y,width,height,MinValue, MaxValue, Title, Data Array, AutoScale, ChartMode)
    DrawGraph(gx + 0 * gap, gy, gwidth, gheight, 900, 1050,
              TXT_PRESSURE_HPA if Units == "M" else TXT_PRESSURE_IN,
              pressure_readings, max_readings, autoscale_on, barchart_off)
    DrawGraph(gx + 1 * gap, gy, gwidth, gheight, 10, 30,
              TXT_TEMPERATURE_C if Units == "M" else TXT_TEMPERATURE_F,
              temperature_readings, max_readings, autoscale_on, barchart_off)
    DrawGraph(gx + 2 * gap, gy, gwidth, gheight, 0, 100, TXT_HUMIDITY_PERCENT,
              humidity_readings, max_readings, autoscale_off, barchart_off)
    if (SumOfPrecip(rain_readings, max_readings) >= SumOfPrecip(snow_readings, max_readings)):
        DrawGraph(gx + 3 * gap + 5, gy, gwidth, gheight, 0, 30,
                  TXT_RAINFALL_MM if Units == "M" else TXT_RAINFALL_IN,
                  rain_readings, max_readings, autoscale_on, barchart_on)
    else:
        DrawGraph(gx + 3 * gap + 5, gy, gwidth, gheight, 0, 30,
                  TXT_SNOWFALL_MM if Units == "M" else TXT_SNOWFALL_IN,
                  snow_readings, max_readings, autoscale_on, barchart_on)
    del pressure_readings, temperature_readings, humidity_readings, \
    rain_readings, snow_readings

def SumOfPrecip(DataArray, readings):
    sum = 0
    for i in DataArray:
        sum += i
    return sum


def DisplayForecastWeather(x, y, index, forcast):
    WxForecast = forcast['list']
    fwidth = const(90)
    x = x + fwidth * index
    DisplayConditionsSection(x + fwidth / 2, y + 90,
                             WxForecast[index]["weather"][0]["icon"], SmallIcon)
    setFont(FiraSansRegular10pt)
    drawString(x + fwidth / 2, y + 30, ConvertUnixTime(
        WxForecast[index]["dt"] + forcast["city"]["timezone"])[0: 5], CENTER)
    drawString(x + fwidth / 2, y + 125, '{:.0f}°/{:.0f}°'.format(
        WxForecast[index]["main"]["temp_max"],
        WxForecast[index]["main"]["temp_min"]), CENTER)


def DisplayConditionsSection(x, y, IconName, IconSize):
    print("Icon name: " + IconName)
    if (IconName == "01d" or IconName == "01n"):
        Sunny(x, y, IconSize, IconName)
    elif (IconName == "02d" or IconName == "02n"):
        MostlySunny(x, y, IconSize, IconName)
    elif (IconName == "03d" or IconName == "03n"):
        Cloudy(x, y, IconSize, IconName)
    elif (IconName == "04d" or IconName == "04n"):
        MostlySunny(x, y, IconSize, IconName)
    elif (IconName == "09d" or IconName == "09n"):
        ChanceRain(x, y, IconSize, IconName)
    elif (IconName == "10d" or IconName == "10n"):
        Rain(x, y, IconSize, IconName)
    elif (IconName == "11d" or IconName == "11n"):
        Tstorms(x, y, IconSize, IconName)
    elif (IconName == "13d" or IconName == "13n"):
        Snow(x, y, IconSize, IconName)
    elif (IconName == "50d"):
        Haze(x, y, IconSize, IconName)
    elif (IconName == "50n"):
        Fog(x, y, IconSize, IconName)
    else:
        Nodata(x, y, IconSize, IconName)


def DisplayForecastTextSection(x, y, weather, forcast):
    WxForecast = forcast['list']
    lineWidth = 34
    setFont(FiraSansRegular12pt)
    # handle weather description field
    Wx_Description = weather["weather"][0]["description"]
    Wx_Description.replace(".", "") # remove any '.'
    spaceRemaining = Wx_Description.find(" ")
    if spaceRemaining == -1:
        spaceRemaining = 0
    if len(Wx_Description) > lineWidth - 1:
        Wx_Description = '{}~{}'.format(Wx_Description[0 : spaceRemaining],
                                        Wx_Description.substring[spaceRemaining + 1 : spaceRemaining + 2])

    try:
        if WxForecast[0]["rain"]["3h"] > 0:
            Wx_Description += ' ({:.1f}{})'.format(WxForecast[0]["rain"]["3h"], "mm" if Units == "M" else "in")
    except:
        pass

    if Wx_Description.find("~") == -1:
        try:
            drawString(x + 30, y + 5, Wx_Description.title(), LEFT)
        except:
            drawString(x + 30, y + 5, Wx_Description, LEFT)
    else:
        drawString(x + 30, y + 5, Wx_Description[0: Wx_Description.find("~")], LEFT)
        drawString(x + 30, y + 30, Wx_Description[Wx_Description.find("~") + 1:], LEFT)


def pressure_trend(forcast):
    trend = forcast["list"][0]["main"]["pressure"] - forcast["list"][2]["main"]["pressure"] # Measure pressure slope between ~now and later
    trend = int(trend * 10 / 10.0) # Remove any small variations less than 0.1
    if trend > 0:
        return "+"
    if trend < 0:
        return "-"
    if trend == 0:
        return "0"
    return "="


def DisplayPressureSection(x, y, weather, forcast):
    setFont(FiraSansRegular12pt)
    slope = pressure_trend(forcast)
    DrawPressureAndTrend(x - 25, y + 10, weather["main"]["pressure"], slope)
    if weather["visibility"] > 0:
        Visibility(x + 145, y, str(weather["visibility"]) + "M")
        x += 150  # Draw the text in the same positions if one is zero, otherwise in-line
    if weather["clouds"]["all"] > 0:
        CloudCover(x + 145, y, weather["clouds"]["all"])


def DrawPressureAndTrend(x, y, pressure, slope):
    if Units == "M":
        drawString(x + 25, y - 10, '{:.0f}hPa'.format(pressure), LEFT)
    else:
        drawString(x + 25, y - 10, '{:.1f}in'.format(pressure), LEFT)
    if slope == "+":
        DrawSegment(x, y, 0, 0, 8, -8, 8, -8, 16, 0)
        DrawSegment(x - 1, y, 0, 0, 8, -8, 8, -8, 16, 0)
    elif slope == "0":
        DrawSegment(x, y, 8, -8, 16, 0, 8, 8, 16, 0)
        DrawSegment(x - 1, y, 8, -8, 16, 0, 8, 8, 16, 0)
    elif slope == "-":
        DrawSegment(x, y, 0, 0, 8, 8, 8, 8, 16, 0)
        DrawSegment(x - 1, y, 0, 0, 8, 8, 8, 8, 16, 0)


def DrawSegment(x, y, o1, o2, o3, o4, o11, o12, o13, o14):
    framebuf.line(x + o1, y + o2, x + o3, y + o4, Black)
    framebuf.line(x + o11, y + o12, x + o13, y + o14, Black)


def DisplayTemperatureSection(x, y, weather):
    setFont(FiraSansRegular18pt)
    drawString(x - 30, y, '{:.1f}°    {:.0f}%'.format(
        weather["main"]["temp"], weather["main"]["humidity"]), LEFT)
    setFont(FiraSansRegular12pt)
    drawString(x + 10, y + 35, '{:.0f}° | {:.0f}°'.format(
        weather["main"]["temp_max"], weather["main"]["temp_min"]), CENTER)  # Show forecast high and Low


def ConvertUnixTime(unix_time):
    # Returns either '21:12  ' or ' 09:12pm' depending on Units mode
    global Units
    now_tm = localtime(unix_time)
    if Units == "M":
        # "%H:%M %d/%m/%y"
        return "{:0>2d}:{:0>2d} {:d}/{:0>2d}/{:0>2d}".format(now_tm[3], now_tm[4],
                now_tm[2], now_tm[1], now_tm[0])
    else:
        # "%I:%M%P %m/%d/%y"
        return "{:0>2d}:{:0>2d}{:s} {:0>d}/{:0>d}/{:d}".format(now_tm[3]%12, now_tm[4], 
                "AM" if now_tm[3]/12 == 0 else "PM", now_tm[2], now_tm[1], now_tm[0])


def arrow(x, y, asize, aangle, pwidth, plength):
    dx = (asize - 10) * cos((aangle - 90) *
                            pi / 180) + x  # calculate X position
    dy = (asize - 10) * sin((aangle - 90) *
                            pi / 180) + y  # calculate Y position
    x1 = 0
    y1 = plength
    x2 = pwidth / 2
    y2 = pwidth / 2
    x3 = -pwidth / 2
    y3 = pwidth / 2
    angle = aangle * pi / 180 - 135
    xx1 = floor(x1 * cos(angle) - y1 * sin(angle) + dx)
    yy1 = floor(y1 * cos(angle) + x1 * sin(angle) + dy)
    xx2 = floor(x2 * cos(angle) - y2 * sin(angle) + dx)
    yy2 = floor(y2 * cos(angle) + x2 * sin(angle) + dy)
    xx3 = floor(x3 * cos(angle) - y3 * sin(angle) + dx)
    yy3 = floor(y3 * cos(angle) + x3 * sin(angle) + dy)
    framebuf.fill_triangle(xx1, yy1, xx3, yy3, xx2, yy2, Black)


def DrawRSSI(x, y, rssi):
    WIFIsignal = 0
    xpos = 1
    for _rssi in range(-100, rssi + 1, 20):
        if _rssi <= -20:
            WIFIsignal = 30
        if _rssi <= -40:
            WIFIsignal = 24
        if _rssi <= -60:
            WIFIsignal = 18
        if _rssi <= -80:
            WIFIsignal = 12
        if _rssi <= -100:
            WIFIsignal = 6
        framebuf.fill_rect(x + xpos * 8, y - WIFIsignal, 6, WIFIsignal, Black)
        xpos += 1


def DrawBattery(x, y, voltage):
    percentage = 100
    if voltage > 1:
        percentage = 2836.9625 * pow(voltage, 4) - 43987.4889 * pow(voltage, 3) + \
                     255233.8134 * pow(voltage, 2) - 656689.7123 * voltage + \
                     632041.7303
        if (voltage >= 4.20):
            percentage = 100
        if (voltage <= 3.20):
            percentage = 0
        framebuf.rect(x + 25, y - 14, 40, 15, Black)
        framebuf.fill_rect(x + 65, y - 10, 4, 7, Black)
        framebuf.fill_rect(x + 27, y - 12, int(36 * percentage / 100.0), 11, Black)
        drawString(x + 85, y - 14,
                   "{:.0f}%  {:.1f}v".format(percentage, voltage), LEFT)


def addcloud(x, y, scale, linesize):
    '''Symbols are drawn on a relative 10x10grid and 1 scale unit = 1 drawing unit
    '''
    framebuf.fill_circle(x - scale * 3, y, scale,
               Black)  # Left most circle
    # Right most circle
    framebuf.fill_circle(x + scale * 3, y, scale, Black)
    # left middle upper circle
    framebuf.fill_circle(x - scale, y - scale, scale * 1.4, Black)
    # Right middle upper circle
    framebuf.fill_circle(x + scale * 1.5, y - scale * 1.3, scale * 1.75, Black)
    framebuf.fill_rect(x - scale * 3 - 1, y - scale, scale * 6,
             scale * 2 + 1, Black)  # Upper and lower lines
    # Clear left most circle
    framebuf.fill_circle(x - scale * 3, y, scale - linesize, White)
    # Clear right most circle
    framebuf.fill_circle(x + scale * 3, y, scale - linesize, White)
    # left middle upper circle
    framebuf.fill_circle(x - scale, y - scale, scale * 1.4 - linesize, White)
    framebuf.fill_circle(x + scale * 1.5, y - scale * 1.3, scale * 1.75 - linesize,
               White)  # Right middle upper circle
    framebuf.fill_rect(x - scale * 3 + 2, y - scale + linesize - 1, scale * 5.9,
             scale * 2 - linesize * 2 + 2, White)  # Upper and lower lines


def addrain(x, y, scale, IconSize):
    if IconSize == SmallIcon:
        setFont(FiraSansRegular8pt)
        drawString(x - 25, y + 12, "///////", LEFT)
    else:
        setFont(FiraSansRegular18pt)
        drawString(x - 60, y + 25, "///////", LEFT)


def addsnow(x, y, scale, IconSize):
    if IconSize == SmallIcon:
        setFont(FiraSansRegular8pt)
        drawString(x - 25, y + 15, "* * * *", LEFT)
    else:
        setFont(FiraSansRegular18pt)
        drawString(x - 60, y + 30, "* * * *", LEFT)


def addtstorm(x, y, scale):
    y = y + floor(scale / 2)
    for i in range(0, 5):
        framebuf.line(x - scale * 4 + scale * i * 1.5 + 0, y + scale * 1.5,
                 x - scale * 3.5 + scale * i * 1.5 + 0, y + scale, Black)
        if scale != Small:
            framebuf.line(x - scale * 4 + scale * i * 1.5 + 1, y + scale * 1.5,
                     x - scale * 3.5 + scale * i * 1.5 + 1, y + scale, Black)
            framebuf.line(x - scale * 4 + scale * i * 1.5 + 2, y + scale * 1.5,
                     x - scale * 3.5 + scale * i * 1.5 + 2, y + scale, Black)
        framebuf.line(x - scale * 4 + scale * i * 1.5, y + scale * 1.5 + 0,
                 x - scale * 3 + scale * i * 1.5 + 0, y + scale * 1.5 + 0, Black)
        if scale != Small:
            framebuf.line(x - scale * 4 + scale * i * 1.5, y + scale * 1.5 + 1,
                     x - scale * 3 + scale * i * 1.5 + 0, y + scale * 1.5 + 1, Black)
            framebuf.line(x - scale * 4 + scale * i * 1.5, y + scale * 1.5 + 2,
                     x - scale * 3 + scale * i * 1.5 + 0, y + scale * 1.5 + 2, Black)
        framebuf.line(x - scale * 3.5 + scale * i * 1.4 + 0, y + scale * 2.5,
                 x - scale * 3 + scale * i * 1.5 + 0, y + scale * 1.5, Black)
        if scale != Small:
            framebuf.line(x - scale * 3.5 + scale * i * 1.4 + 1, y + scale * 2.5,
                     x - scale * 3 + scale * i * 1.5 + 1, y + scale * 1.5, Black)
            framebuf.line(x - scale * 3.5 + scale * i * 1.4 + 2, y + scale * 2.5,
                     x - scale * 3 + scale * i * 1.5 + 2, y + scale * 1.5, Black)


def addsun(x, y, scale, IconSize):
    linesize = 5
    framebuf.fill_rect(x - scale * 2, y, scale * 4, linesize, Black)
    framebuf.fill_rect(x, y - scale * 2, linesize, scale * 4, Black)
    framebuf.line(x - scale * 1.3, y - scale * 1.3, x +
             scale * 1.3, y + scale * 1.3, Black)
    framebuf.line(x - scale * 1.3, y + scale * 1.3, x +
             scale * 1.3, y - scale * 1.3, Black)
    if IconSize == LargeIcon:
        framebuf.line(1 + x - scale * 1.3, y - scale * 1.3, 1 +
                 x + scale * 1.3, y + scale * 1.3, Black)
        framebuf.line(2 + x - scale * 1.3, y - scale * 1.3, 2 +
                 x + scale * 1.3, y + scale * 1.3, Black)
        framebuf.line(3 + x - scale * 1.3, y - scale * 1.3, 3 +
                 x + scale * 1.3, y + scale * 1.3, Black)
        framebuf.line(1 + x - scale * 1.3, y + scale * 1.3, 1 +
                 x + scale * 1.3, y - scale * 1.3, Black)
        framebuf.line(2 + x - scale * 1.3, y + scale * 1.3, 2 +
                 x + scale * 1.3, y - scale * 1.3, Black)
        framebuf.line(3 + x - scale * 1.3, y + scale * 1.3, 3 +
                 x + scale * 1.3, y - scale * 1.3, Black)
    framebuf.fill_circle(x, y, scale * 1.3, White)
    framebuf.fill_circle(x, y, scale, Black)
    framebuf.fill_circle(x, y, scale - linesize, White)


def addfog(x, y, scale, linesize, IconSize):
    if IconSize == SmallIcon:
        y -= 10
        linesize = 1
    for i in range(0, 6):
        framebuf.fill_rect(x - scale * 3, y + scale * 1.5, scale * 6, linesize, Black)
        framebuf.fill_rect(x - scale * 3, y + scale * 2.0, scale * 6, linesize, Black)
        framebuf.fill_rect(x - scale * 3, y + scale * 2.5, scale * 6, linesize, Black)


def Sunny(x, y, IconSize, IconName):
    scale = Small
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    else:
        y = y - 3  # Shift up small sun icon
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    scale = scale * 1.6
    addsun(x, y, scale, IconSize)


def MostlySunny(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addsun(x - scale * 1.8, y - scale * 1.8, scale, IconSize)
    addcloud(x, y, scale, linesize)


def MostlyCloudy(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addsun(x - scale * 1.8, y - scale * 1.8, scale, IconSize)


def Cloudy(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x + 15, y - 22, scale / 2, linesize)  # Cloud top right
    addcloud(x - 10, y - 18, scale / 2, linesize)  # Cloud top left
    addcloud(x, y, scale, linesize)               # Main cloud


def Rain(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addrain(x, y, scale, IconSize)


def ExpectRain(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addsun(x - scale * 1.8, y - scale * 1.8, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addrain(x, y, scale, IconSize)


def ChanceRain(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addsun(x - scale * 1.8, y - scale * 1.8, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addrain(x, y, scale, IconSize)


def Tstorms(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addtstorm(x, y, scale)


def Snow(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x, y, scale, linesize)
    addsnow(x, y, scale, IconSize)


def Fog(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addcloud(x, y - 5, scale, linesize)
    addfog(x, y - 5, scale, linesize, IconSize)


def Haze(x, y, IconSize, IconName):
    scale = Small
    linesize = 5
    Offset = 10
    if IconSize == LargeIcon:
        scale = Large
        Offset = 35
    if IconName.endswith("n"):
        addmoon(x, y + Offset, scale, IconSize)
    addsun(x, y - 5, scale * 1.4, IconSize)
    addfog(x, y - 5, scale * 1.4, linesize, IconSize)


def CloudCover(x, y, CCover):
    addcloud(x - 9, y + 2, Small * 0.3, 2)  # Cloud top left
    addcloud(x + 3, y - 2, Small * 0.3, 2)  # Cloud top right
    addcloud(x, y + 10, Small * 0.6, 2)    # Main cloud
    drawString(x + 20, y, "{:d}%".format(CCover), LEFT)


def Visibility(x, y, Visi):
    start_angle = 0.52
    end_angle = 2.61
    Offset = 8
    r = 14
    # for i in range(start_angle, end_angle, 0.05):
    i = start_angle
    while i < end_angle:
        framebuf.pixel(x + r * cos(i), y - r / 2 + r * sin(i) + Offset, Black)
        framebuf.pixel(x + r * cos(i), 1 + y - r / 2 + r * sin(i) + Offset, Black)
        i += 0.05
    start_angle = 3.61
    end_angle = 5.78
    # for i in range(start_angle, end_angle, 0.05):
    i = start_angle
    while i < end_angle:
        framebuf.pixel(x + r * cos(i), y + r / 2 + r * sin(i) + Offset, Black)
        framebuf.pixel(x + r * cos(i), 1 + y + r / 2 + r * sin(i) + Offset, Black)
        i += 0.05
    framebuf.fill_circle(x, y + Offset, r / 4, Black)
    drawString(x + 20, y, Visi, LEFT)


def addmoon(x, y, scale, IconSize):
    if IconSize == LargeIcon:
        framebuf.fill_circle(x - 85, y - 100, floor(scale * 0.8), Black)
        framebuf.fill_circle(x - 57, y - 100, floor(scale * 1.6), White)
    else:
        framebuf.fill_circle(x - 28, y - 37, floor(scale * 1.0), Black)
        framebuf.fill_circle(x - 20, y - 37, floor(scale * 1.6), White)


def Nodata(x, y, IconSize, IconName):
    if IconSize == LargeIcon:
        setFont(FiraSansRegular24pt)
    else:
        setFont(FiraSansRegular12pt)
    drawString(x - 3, y - 10, "?", CENTER)


def DrawGraph(x_pos, y_pos, gwidth, gheight, Y1Min, Y1Max, title, DataArray, 
              readings, auto_scale, barchart_mode):
    '''This function will draw a graph on a ePaper/TFT/LCD display using data
    from an array containing data to be graphed.
    '''
    # Sets the autoscale increment, so axis steps up fter a change of e.g. 3
    auto_scale_margin = const(0)
    y_minor_axis = const(5)      # 5 y-axis division markers
    setFont(FiraSansRegular10pt)
    maxYscale = -10000
    minYscale = 10000
    last_x = 0
    last_y = 0
    x2 = 0.0
    y2 = 0.0
    if auto_scale == True:
        for i in range(1, readings):
            if DataArray[i] >= maxYscale:
                maxYscale = DataArray[i]
            if DataArray[i] <= minYscale:
                minYscale = DataArray[i]

        '''Auto scale the graph and round to the nearest value defined, default
        was Y1Max.
        '''
        maxYscale = round(maxYscale + auto_scale_margin, 1)
        Y1Max = round(maxYscale + 0.5, 1)
        if minYscale != 0:
            '''Auto scale the graph and round to the nearest value defined,
            default was Y1Min
            '''
            minYscale = round(minYscale - auto_scale_margin, 1)
        Y1Min = round(minYscale, 1)

    # Draw the graph
    last_x = x_pos + 1
    last_y = y_pos + (Y1Max - constrain(DataArray[1], Y1Min, Y1Max)) / (Y1Max - Y1Min) * gheight

    framebuf.rect(x_pos, y_pos, gwidth + 3, gheight + 2, Grey)
    drawString(x_pos - 20 + gwidth / 2, y_pos - 28, title, CENTER)
    for gx in range(0, readings):
        '''max_readings is the global variable that sets the maximum data that
        can be plotted
        '''
        x2 = x_pos + gx * gwidth / (readings - 1) - 1
        y2 = y_pos + (Y1Max - constrain(DataArray[gx], Y1Min, Y1Max)) / (Y1Max - Y1Min) * gheight + 1
        if barchart_mode:
            framebuf.fill_rect(last_x + 2, y2, (gwidth / readings) - 1,
                               y_pos + gheight - y2 + 2, Black)
        else:
            # Two lines for hi-res display
            # print("last_x: {:d}, (last_y - 1): {:d}, x2: {:d}, y2 - 1: {:d}".format(int(last_x),
            #       int(last_y - 1), int(x2), int(y2 - 1)))
            # print("last_x: {:d}, last_y: {:d}, x2: {:d}, y2: {:d}".format(int(last_x),
            #       int(last_y), int(x2), int(y2)))
            framebuf.line(last_x, last_y - 1, x2, y2 - 1, Black)
            framebuf.line(last_x, last_y, x2, y2, Black)
        last_x = int(x2)
        last_y = int(y2)

    # Draw the Y-axis scale
    number_of_dashes = const(20)
    for spacing in range(0, y_minor_axis + 1):
        for j in range(0, number_of_dashes):
            '''Draw dashed graph grid lines'''
            if spacing < y_minor_axis:
                framebuf.hline((x_pos + 3 + j * gwidth / number_of_dashes),
                              y_pos + (gheight * spacing / y_minor_axis),
                              gwidth / (2 * number_of_dashes), Grey)
        if (int(Y1Max - (Y1Max - Y1Min) / y_minor_axis * spacing) < 5 or title == TXT_PRESSURE_IN):
            drawString(x_pos - 10, y_pos + gheight * spacing / y_minor_axis - 5,
                       "{:.1f}".format(
                           (Y1Max - (float)(Y1Max - Y1Min) / y_minor_axis * spacing + 0.01)),
                       RIGHT)
        else:
            if Y1Min < 1 and Y1Max < 10:
                drawString(x_pos - 3,
                           y_pos + gheight * spacing / y_minor_axis - 5,
                           "{:.1f}".format(
                               (Y1Max - (float)(Y1Max - Y1Min) / y_minor_axis * spacing + 0.01)),
                           RIGHT)
            else:
                drawString(x_pos - 7,
                           y_pos + gheight * spacing / y_minor_axis - 5,
                           "{:d}".format(
                               int(Y1Max - (Y1Max - Y1Min) / y_minor_axis * spacing + 0.01)),
                           RIGHT)

    for i in range(0, 3):
        drawString(20 + x_pos + gwidth / 3 * i, y_pos +
                   gheight + 10, "{:d}d".format(i), LEFT)
        if i < 2:
            framebuf.vline(x_pos + gwidth / 3 * i + gwidth /
                          3, y_pos, gheight, LightGrey)


def drawString(x, y, text, align):
    global currentFont
    x = int(x)
    y = int(y)
    # print("x {:d} y {:d}".format(int(x), int(y)))

    x1 = 0
    y1 = 0
    w = 0
    h = 0
    xx = x
    yy = y
    xx, yy, x1, y1, w, h = framebuf.get_text_bounds(
        currentFont, text, xx, yy, x1, y1, w, h)
    # print("w {:d}".format(int(w)))
    if align == RIGHT:
        x = x - w
    if align == CENTER:
        x = x - w / 2
    cursor_y = y + h

    # print("x {:d} cursor_y {:d}".format(int(x), int(cursor_y)))

    framebuf.text(currentFont, text, x, cursor_y)


def fillRect(x, y, w, h, color):
    framebuf.fill_rect(x, y, w, h, color)


def fillTriangle(x0, y0, x1, y1, x2, y2, color):
    framebuf.fill_triangle(x0, y0, x1, y1, x2, y2, color)


def drawCircle(x0, y0, r, color):
    framebuf.circle(x0, y0, r, color)


def drawRect(x, y, w, h, color):
    framebuf.rect(x, y, w, h, color)


def fillCircle(x, y, r, color):
    framebuf.fill_circle(x, y, r, color)


def drawFastHLine(x0, y0, length, color):
    framebuf.hline(x0, y0, length, color)


def drawFastVLine(x0, y0, length, color):
    framebuf.vline(x0, y0, length, color)


def drawLine(x0, y0, x1, y1, color):
    framebuf.line(x0, y0, x1, y1, color)


def drawPixel(x, y, color):
    x = int(x)
    y = int(y)
    framebuf.pixel(x, y, color)


def setFont(font):
    global currentFont
    currentFont = font


def constrain(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def DisplayWeather(weather, forcast, rssi, voltage):
    DisplayStatusSection(600, 20, rssi, voltage)
    DisplayGeneralInfoSection(weather)
    DisplayDisplayWindSection(137, 150, weather["wind"]["deg"],
                              weather["wind"]["speed"], 100, Units)
    DisplayAstronomySection(5, 255, weather)
    DisplayMainWeatherSection(320, 110, weather, forcast)
    DisplayWeatherIcon(810, 130, weather)
    DisplayForecastSection(320, 220, forcast)

autoscale_on = True
autoscale_off = False
barchart_on = True
barchart_off = False

# WxConditions = None
# WxForecast = None
Units = 'M'
Hemisphere = "north"

max_readings = 24


if __name__ == "__main__":
    try:
        from machine import ADC,Pin
    except:
        pass

    try:
        from framebuf1 import FrameBuffer
    except:
        from framebuf import FrameBuffer

    import gc
    from json import load
    gc.enable()
    f = open("weather.json", "r")
    weather = load(f)
    f.close()
    p = open("forcast.json", "r")
    forcast = load(p)
    p.close()
    gc.collect()
    buffer = [ 0 for _ in range(0, int(960 * 540 / 2)) ]
    fb1 = FrameBuffer(buffer, 960, 540)
    fb1.fill(255)

    InitUI(fb1)

    try:
        adc = ADC(Pin(36))
        DisplayWeather(weather, forcast, -49, adc.read()/4096.0 * 5)
    except:
        DisplayWeather(weather, forcast, -49, 4.0)

    del weather
    del forcast
    gc.collect()
    try:
        from epd import EPD47
        e = EPD47()
        e.power(True)
        e.clear()
        e.bitmap(buffer, 0, 0, 960, 540)
    except:
        print("The current parser is not micropython")

