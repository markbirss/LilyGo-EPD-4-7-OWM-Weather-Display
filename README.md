# LilyGo-EPD-4-7-OWM-Weather-Display
Using the LilyGo EPD 4.7" display to show OWM Weather Data


Version 2.6 Added real moon image with moon phase overlay.

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
    imgconvert.py -i sourceimagename.jpg - n requiredname -o outputfile.h

10. Example convert sunny.jpg to sunny.h
    imgconvert.py -n sunny -i sunny.jpg -o sunny.h

11. The image file is now created, move the 'sunny.h' file into your sketch folder and include the file in your code like this #include "sunny.h"
12. 
13. Draw the image like this:

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

7.  Transfer the following files to your EPD47 folder - imgconvert.py and fontconvert.py they are located in the EDP47 Library script folder

8.  Install Python 3.91, start a Windows cmd prompt, and chage directory to the folder EPD47:
    cd C:\Users\david\EPD47

9.  To create a Regular 10-point font, enter this at the command prompt:
    fontconvert.py OpenSans10 10 OpenSans-Regular.ttf > opensans10.h

    *** Make sure the Font names are like this: 'OpenSansBnn' note the capitlised O and S and B

10. To create a Bold 10-point font, enter this at the command prompt:
    fontconvert.py OpenSans10B 10  OpenSans-Bold.ttf > opensans10b.h

11. To create a Bold 24-point font, enter this at the command prompt:
    fontconvert.py OpenSans24B 24 OpenSans-Bold.ttf > opensans24b.h

12. The font files are now created, copy them to your sketch folder for use e.g. setFont(fontname);
