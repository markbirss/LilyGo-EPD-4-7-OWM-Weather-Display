# LilyGo-EPD-4-7-OWM-Weather-Display
Using the LilyGo EPD 4.7" display to show OWM Weather Data

For the latest version please use 'contact' at www.dsbird.org.uk for the latest version

<b>*** Sorry but due to piracy I'm no-longer releasing a new version for public use ***</b>

Version 3.8
1. Corrected JSON decoding
2. Used last known forecast when not yet published on day-5
3. When forecast incompleted, added indicator *
4. Add rain / snow reports, displayed when imminent (next 3-hours)

Version 3.7
1. Improved Imperial units and time displaying

Version 3.6
1. Improved graphing routine
2. Added Dewpoint display
3. Used OWM 'Onecall' to get additonal data
4. Improved wind display and corrected Metric and Imperial displays
5. Improved Imperial time displays
6. Improved top-status line alignment and overall look
7. Corrected rainfal / snowfall counting
8. Changed wind direction from 'wind direction from' to 'wind direction to', so now the arrow points to where the wind is blowing towards
9. Added indicator of incomplete forecast, sleep time adjusted to get forecast quicker
10. Changed forecast time regions
11. Fixed UVI index display
12. Fixed rain/snow fall predictions
13. Fixed large and small weather icons
14. Revised all weather icon alignment
15. Corrected Hi/Lo temperature capture function
16. Corrected and rationalised all weather reception codes

Version 2.72
1. Improved Icon shapes and positioning
2. Adjusted Forecast Weather function to improve readability

Version 2.71
1. Which implemented OWM onecall API
2. Improved all weather icons
3. Added sunrise and sunset icons
4. Added UV index and icon
5. Added Feels-Like temperature if wind speed > 0
6. Now now uses LAT/LON for weather location needed for the onecall API call, infact all OWM API calls are better supported with LAT/LON
7. Added one more forecast period, so now displays 24-hours ahead
8. *** NOTE: You need to update **forecast_record.h and owm_credentials.h** from here
9. Add sunset.h, sunrise,h and moon.h to the sketch folder

Select board type: 'ESP32 Dev Module'
Ensure 'PSRAM' is Enabled

Creating images:

1.  On Windows PC install Python 3.91 or later, find it here: https://www.python.org/downloads/

2.  Install Python

5.  Create an accessible folder e.g. EPD47 e.g. C:\EPD47   ***Note this folder must be accessible to the cmd pompt
    A better location might be in your Documents folder usually located at C\Your-Username\Documents, example:
    Directory of C:\Users\david\EPD47

6.  Copy your source .JPG images to the folder e.g. sunny.jpg

7.  Transfer the following files to your EPD47 folder - imgconvert.py and fontconvert.py they are located in the EDP47 Library script folder

8.  Install Python 3.91, start a Windows cmd prompt, and chage directory to the folder EPD47:
    cd C:\Users\david\EPD47

9.  To create an image for display, enter this at the command prompt:

    **imgconvert.py -i sourceimagename.jpg - n requiredname -o outputfile.h**

10. Example convert sunny.jpg to sunny.h

    **imgconvert.py -n sunny -i sunny.jpg -o sunny.h**

11. The image file is now created, move the 'sunny.h' file into your sketch folder and include the file in your code like this #include "sunny.h"

12. Draw the image like this:

DrawSunnyImage(x, y);

void DrawSunnyImage(int x, int y) {
  Rect_t area = {
    .x = x, .y = y, .width  = sunny_width, .height =  sunny_height
  };
  epd_draw_grayscale_image(area, (uint8_t *) sunny_data);
}

Creating fonts:
1.  On Windows PC install Python 3.91 or later, find it here: https://www.python.org/downloads/

2.  Install Python

3.  Find a suitable Font Family e.g google opensans.ttf
    https://fonts.google.com/specimen/Open+Sans

4.  Download the Font Family file

5.  Create an accessible folder e.g. EPD47 e.g. C:\EPD47   ***Note this folder must be accessible to the cmd pompt
    A better location might be in your Documents folder usually located at C\Your-Username\Documents, example:
    Directory of C:\Users\david\EPD47

6.  Unzip all *.ttf files to the EPD47 folder, it now has all types of font files.ttf of the chosen font, e.g. regular, bold italic, etc

    29/01/2021  11:24           595,329 Open_Sans.zip
    
    29/01/2021  11:24           104,120 OpenSans-Bold.ttf
    
    29/01/2021  11:24            92,628 OpenSans-BoldItalic.ttf
    
    29/01/2021  11:24           102,076 OpenSans-ExtraBold.ttf
    
    29/01/2021  11:24            92,772 OpenSans-ExtraBoldItalic.ttf
    
    29/01/2021  11:24            92,240 OpenSans-Italic.ttf
    
    29/01/2021  11:24           101,696 OpenSans-Light.ttf
    
    29/01/2021  11:24            92,488 OpenSans-LightItalic.ttf
    
    29/01/2021  11:24            96,932 OpenSans-Regular.ttf
    
    29/01/2021  11:24           100,820 OpenSans-SemiBold.ttf
    
    29/01/2021  11:24            92,180 OpenSans-SemiBoldItalic.ttf
    
7.  Transfer the following files to your EPD47 folder - **imgconvert.py** and **fontconvert.py** they are located in the EDP47 Library script folder

8.  Install Python 3.91, start a Windows cmd prompt, and chage directory to the folder EPD47:
    cd C:\Users\david\EPD47

9.  To create a Regular 10-point font, enter this at the command prompt:

    **fontconvert.py OpenSans10 10 OpenSans-Regular.ttf > opensans10.h**

    *** Make sure the Font names are like this: 'OpenSansBnn' note the capitlised O and S and B

10. To create a Bold 10-point font, enter this at the command prompt:
    
    **fontconvert.py OpenSans10B 10  OpenSans-Bold.ttf > opensans10b.h**

11. To create a Bold 24-point font, enter this at the command prompt:
    
    **fontconvert.py OpenSans24B 24 OpenSans-Bold.ttf > opensans24b.h**

12. The font files are now created, copy them to your sketch folder for use e.g. setFont(fontname);
