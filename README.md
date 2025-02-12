# FIXATION SOFTWARE FOR IVCM

## Synopsis
This software permit to control the fixation during an examination with the IVCM. It is written for a Raspberry Pi 4 with standard 7"-Display, but can be used with every other Linux or Windows system.

## Version
- V2.5
- Release 02.05.2024

### Major changes of V2
- it is possible to configurate the region around the whorl as wished. The pattern will then be saved and can be used again.
- the distance between the points can be set differently in the whorl as in the rectangle
- with the device from Rostock, it is possible to run sequences automatically without the limit of 100 images: after 100 images and 6 seconds of saving-pause the hrt-sequence will start automatically again.

### Minores changes
#### V 2.0.1
- if width or height of rectangle is set to 0, the pattern stop after the part around the whorl.
- fixated some bugs
#### V 2.1
- loading a pattern, the load window will be close directly, so that it is not behind the main window
- it is possible to set a different distance between points in the whorl region
- it is possible to pause the automate sequence and start it again from the same point
- if you want to use only the pattern that you configurated, set the rectangle width or height to 0.
#### V2.2
- in the automated mode, the points sequence will stop short before 100 pictures are taken. Use the HRT-rate setting parameter.
- Fixation eye is now corrected
#### V2.3
- now it is possible to show the raster on the display before starting the measurement, using the tast <t> or <KP_5>.
#### V2.5
- the device of Rostock is implemented ("virtual pedal") so that during an automated sequence, after 100 images the system will stop and start again after a short break for saving images (both fixation and hrt).
- druing an automated sequence, pressing <Enter> will pause the sequence if it is running and start it again if it is paused.

## Use
### Settings
The default.txt file contein all the default settings, which are directly imported once the software is launched. You are free to change them.

### Determine port for Rostock-plugin
The first time that the plugin will be used, the USB-port should be checked. Default ist USB0. To do so follow the next steps:
1. Plug USB in one port of  Raspberry Pi
2. Open terminal on the top left corner (black icon with white)
3. Write:

    `dmesg | tail` 
4. Read on the output the USB port used by the plugin (one of the last rows, should be USB followed by a number): normally is USB0.
5. If it is USB0, no further steps are needed. If different than USB0, open foot_switch.py document and change the number after USB at the line 11 (ser.port = '/dev/ttyUSB0')
6. Close foot_switch.py saving the changes.

### Starting
No executable is created, the software has to be started from the command line with the following inputs:
1. Open terminal on the top left corner (black icon with white)
2. Make sure to be in the right directory

    `cd Desktop/fixation_v2.5`
3. Start 

    `python3 main.py`

### Start window
Once the software is started, the start window will appear. The following parameters have to be defined. No error is given if some information is missing.
- Fixation Eye: choose the fixation eye
- Distance between points [mm]: insert distance between the points, considering the distance on the screen in millimeters
- Distance between points in the whorl region [mm]: insert distance between the points in the whorl region, considering the distance on the screen in millimeters
- Size of dot [pixel]: insert the size of the fixation dot
- Monitor direction: hor = horizontal (standard position); vert_clock = vertical turned clockwise from the standard position; vert_counter = vertical turned counterclockwise from the standard position
- Movement direction: indicate if the direction commands on the keypad represent the direction on the display or of the plexus
- Screen dimensions [mm]: insert the dimension of the display in millimeters, standard is the standard 7"-display for Raspberry Pi
- Rectangle [images]: dimensions of the rectangle, which has to be imaged, in amount of images
- Distance between whorl and rectangle [images]: insert distance, in images, between the whorl and the start of the rectangle. min = 2, odd numbers will be rounded down to the closest even number
- Number of steps nasally [images]: insert how many steps should be gone nasally.
- How many sec each point [s]: what is the time that every point has to be shown? after this amount of seconds, the next fixation point will be shown
- virtual pedal: checkbox to choose to use the Rostock-device.
- Init. VP: button to initialise connection with HRT. If connection available, pushing the button should take some images on the hrt. If port is not right, an error message will be shown. Check port following steps mentioned above.
- HRT-rate [imgs/s]: it is the images rate for the sequence modality in the hrt. If the fixation sequence is longer than the hrt-sequence, the points sequence will pause short before 100 images are taken.
- Mode: choose if the the sequence should be manual, semiautomated or autoamted.
    - manual: the fixation point can be moved with the keypad
    - semiautomated: the sequence of points is calculated, the examiner press the 'Enter'-key to go to the next point
    - automated: the point move automatically with the defined speed
- starting_point_x: 0 is the left side, 1 is the right side
- starting_point_y: 0 is the upper side, 1 is the lower side
- Patient ID: insert patient ID

### Pattern configuration
There are two buttons: "Config." and "Open"
- the "Config."-button open a window in which it is possible to draw the pattern. 
    - Please read the instruction; the button "Instruction will open a new window with the text.
    - Through the keypad or with the 4 directions buttons the pattern is drawn. Each direction has a distinctive colour, only to make it easy to recognize the right sequence, in which the points have been inserted.
    - Reset-button: all the points are erased without being saved.
    - Close-button: the window will be close without saving the data.
    - Input-field: please insert the name of the pattern, so that a unique file is created
    - Save-button: the pattern is saved in the file, the window closed and the pattern is loaded to be used.
    - pressing <Enter>, the pattern will be saved
    - pressing <Escape>, the window is closed without saving the pattern
- the "Open"-button permit to choose a file with a pattern created in the past.
    - with the "..."-button choose an existing pattern
    - Open-button: load the pattern in the software
    - select the checkbox, if you want that this pattern is loaded everytime the software is launched.
    - IMPORTANT: this checkbos has to be selected before choosing the file

### Test window
At the beginning, a yellow rectangle is shown in the middle of the screen, as start point. The examiner has to move the fixation point (which become a point) until the inferior whorl is seen.
From there, dependent from the mode, the IVCM measurement will start.

In automated mode only:
- pressing the button <Enter>, <Subtract> on the keypad or <a>, the sequence will stop on the last point showed. Pressing <Enter>, the sequence will be resumed from the same point.

In automated and semi-automated mode:
- pressing the button <t> (like 'test') or <KP_5> (the number 5) on the keypad, the whole raster is shown in orange on the display. The sequence can be started with <Return>, like always.

#### Manual Mode
The examiner can move the point as wished, using the keypad. No raster plot will be saved. 

#### Semi-automated Mode
After the inferior whorl is found, pressing <Enter> all the point of the raster will be showed one after the other. Important: to go to next point <Enter> has to be pressed

#### Automated Mode
After the inferior whorl is found, pressing <Enter> the raster-points are shown one after another in interval matching the inserted value.

##### Virtual pedal
If the Rostock-Plugin is used, the sequence will stop to let time to the hrt to save the sequence and start again automatically, until all points are shown.

#### Terminating
In any case, pressing <Escape> the Test window will be closed.

## Important
if during the sequence the points are outside of the display, no notice will be given. 

## Authorship
Emanuele Käser

Istitute of Optometry, FHNW

Olten, Switzerland

emanuele.kaeser@fhnw.ch

+41 62 957 23 02