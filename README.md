# Gcode tumbnail generator for Simplify3D and others
Encode the image of the stl model in the gcode file. Compatible with Simplify3D and others


# INSTALLATION (for windows)
Download and install OpenScad (https://openscad.org/downloads.html).

Install python3 and pip

Open cmd and install python dependencies with pip:

pip install PyQt5 numpy argparse pillow

Download the python script from this repository and save in on the computer in a non root folder (for example save it in the documents or on the desktop).
Open Simplify3D, open the process settings and at the bottom of the script tab, in the post-processing commands area, add the following line:

python "C:\Users\fabio\Desktop\StlToImg\StlToImg.py" --gcodename "[output_filepath]" 

Where "C:\Users\fabio\Desktop\StlToImg\StlToImg.py" MUST be replaced with the path you have chosen for the file.

You can also run the code manually by witing the line in a cmd window and by replacing "[output_filepath]" with the path of the gcode file.

![image](https://user-images.githubusercontent.com/76878512/178706122-4931561a-a943-4328-bcd6-74f3e6082248.png)

Thats it, when you export the gcode a tumbnail of the 3D model will be added at the top of the gcode file.
I've tested it with klipper and it works without issues.

![image](https://user-images.githubusercontent.com/76878512/178697824-9cb6ff84-b9ea-45eb-8931-c2e3906ec053.png)


# FOR LINUX
The same as above but you will need to open the file and change the default path for the openscad.com file and few other parts (such as replace "\\" with "/"),
I will try to upload a linux version of the code as soon as I can get around it.

# LIMITATIONS
The name of the gcode file must be the same of the stl file (ex: for file cube.stl the gcode must be called cube.gcode) otherwise the program is not going to be able to load the stl file and it will add a black image in the gcode (Simplify3D does not provide an [input_filepath] variables to pass the stl input name to the code so I'm obtaining the stl file name from the gcode file name).

The gcode file MUST me exported in the same folder where the stl file resides (for the same reason above), otherwise you can add the --stlname argument and manually select the stl file as shown in the advanced control section below.

The code can process only one stl file at the same time.

# ADVANCED CONTROL
I've added a few arguments to the python code to customize different variables:

to select the resolution use the arguments: --height [height] --width [width] (ex: --height 300 --width 300). The default is 400x400.

to manually select the stl file path (if the stl file is not in the same folder of the gcode file or if it has a different name) use the argument: --stlname [path]

to select the directory of the openscad.com executable use the argument: --path [path] (default is: "C:\\Program Files\\OpenSCAD\\openscad.com")

to select the code working directory (the place where the code will save the temporary files): --codepath [path] (the default is the directory where the code is saved)

# COMPILE IN EXE
To compile the python code in a single executable file:

pip install pyinstaller

pyinstaller --onefile StlToImg.py

This will create an exe file in the dist folder containing all the required components to run the python script (keep in mind that executing the code in this way will increase the runtime).

Then change the line in Simplify3D with:

python "C:\Users\fabio\Desktop\StlToImg\StlToImg.exe" --gcodename "[output_filepath]" 

