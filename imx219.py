import os
import subprocess
from datetime import datetime
from PIL import Image
from glob import glob

width = str(800)
height = str(600)
avg_brightness = str(0)
gain = str(1)
shutter = str(1000)

while True:

    time = datetime.now()
    years = int(time.year)
    months = int(time.month)
    days = int(time.day)
    hours = int(time.hour)
    minutes = int(time.minute)
    seconds = int(time.second)

    dir = "/home/pi/test/" + str(years) + str(months).zfill(2) + str(days).zfill(2) + "/"
    subprocess.run(["mkdir", "-p", dir], stderr=subprocess.DEVNULL)

    filename = dir + str(years) + str(months).zfill(2) + str(days).zfill(2) + "-" + str(hours).zfill(2) + str(minutes).zfill(2) + str(seconds).zfill(2) + "-" + gain + "-" + shutter + "-" + avg_brightness + ".jpg"
    #print("file name: " + filename)
    subprocess.run(["rpicam-still", "-v", "0", "-o", filename, "-t", "5", "--gain", gain, "--shutter", shutter, "--width", width, "--height", height, "--framerate", "1", "--awb", "auto", "--metering", "spot", "--tuning-file", "/usr/share/libcamera/ipa/rpi/vc4/imx219_noir.json"], stderr=subprocess.DEVNULL)

    files = glob(dir + str(years) + str(months).zfill(2) + str(days).zfill(2) + "-" + str(hours).zfill(2) + str(minutes).zfill(2) + "*.jpg")
    latest = max(files, key=os.path.getmtime)
    #print("latest name: " + latest)
    img = Image.open(latest).convert("L")
    pixels = list(img.getdata())
    avg_brightness = sum(pixels) / len(pixels)

    avg_brightness = int(avg_brightness)
    gain = int(gain)
    shutter = int(shutter)

    if avg_brightness >= 0 and avg_brightness < 15:
        if gain < 15:
            gain = gain + 1
        shutter = shutter + 2000
    elif avg_brightness > 191 and avg_brightness <= 255:
        if gain > 1:
            gain = gain - 1
        shutter = shutter - 2000
        if shutter < 0:
            shutter = 0

    avg_brightness = str(avg_brightness)
    gain = str(gain)
    shutter = str(shutter)
    #print("average brightness: " + avg_brightness)
    #print("gain value: " + gain)
    #print("shutter value: " + shutter)
