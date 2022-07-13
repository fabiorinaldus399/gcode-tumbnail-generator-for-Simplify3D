## Written By Fabio Rinaldini

import os
import argparse
from PIL import Image
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QBuffer
import base64
        
parser = argparse.ArgumentParser(description='Gcode image encoder')
parser.add_argument('--gcodename', type=str, default="",
                    help='the path of the gcode file')
parser.add_argument('--stlname', type=str, default="",
                    help='the path of the stl file')
parser.add_argument('--height', type=int, default=400,
                    help='the height of the image')
parser.add_argument('--width', type=int, default=400,
                    help='the width of the image')
parser.add_argument('--path', type=str, default='"/usr/bin/openscad',
                    help='the path of Openscad')
parser.add_argument('--codepath', type=str, default=os.getcwd(),
                    help='the path for the code working directory')
args = parser.parse_args()
os.chdir(args.codepath)
height = args.height
width = args.width

gcodename = args.gcodename
if not os.path.exists(gcodename):
    raise Exception ("Unable to find the gcode file " + gcodename)

if args.stlname == "":
    stlname = gcodename[:-6] + ".stl"
else:
    stlname = args.stlname
if not os.path.exists(stlname):
    raise Exception ("Unable to find the stl file " + stlname)

stlname = stlname.replace("\\", "/")
print("Stl file name: " + stlname)         
print("Gcode file name: " + gcodename)
     
with open ("command.scad", 'w') as openscad_command:
     openscad_command.write('import("' + stlname + '");')
command = args.path + " ./command.scad -o ./image.png --autocenter --viewall --colorscheme=Starnight --imgsize=" + str(height) + "," + str(width) + '"'
print(command)
os.system('"' + command + '"')

image = "./image.png"

##encode image in gcode
print("Starting image encoding...")

def convertImage(image):
    return QImage(image)
    
def encodeImage(conv_image):
    thumbnail_buffer = QBuffer()
    thumbnail_buffer.open(QBuffer.ReadWrite)
    thumbnail_image = conv_image
    thumbnail_image.save(thumbnail_buffer, "JPG")
    base64_bytes = base64.b64encode(thumbnail_buffer.data())
    base64_message = base64_bytes.decode('ascii')
    thumbnail_buffer.close()
    return base64_message

def convertImageToGcode(encoded_image, width, height, chunk_size=78):
    gcode = []

    encoded_image_length = len(encoded_image)
    gcode.append(";")
    gcode.append("; thumbnail begin {}x{} {}".format(
        width, height, encoded_image_length))
    chunks = ["; {}".format(encoded_image[i:i+chunk_size])
        for i in range(0, len(encoded_image), chunk_size)]
    gcode.extend(chunks)
    gcode.append("; thumbnail end")
    gcode.append(";")
    gcode.append("; image encoded with STI")
    gcode.append(";")
    gcode.append("")
    return gcode

def execute(data):

    conv_image = convertImage(image)
    if conv_image:
        encoded_image = encodeImage(conv_image)
        image_gcode = convertImageToGcode(
            encoded_image, width, height)

        with open("./image.gcode", "w") as gcode_mg:
            for line in image_gcode:
              gcode_mg.write("%s\n" % line)
            print("Image successfully encoded in gcode")
        with open("image.gcode", 'r') as fp1:
            filedata = fp1.read()       
        with open(data, 'r') as fp2:
            filedata2 = fp2.read() 
        filedata += "\n"
        filedata += filedata2

        with open (data, 'w') as fp:
            fp.write(filedata)
        
        os.remove("./image.gcode")
        os.remove("./command.scad")
        os.remove("./image.png")
        
    print("Done")

execute(gcodename)       
