#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import random
import platform
import subprocess
from image_to_binary import *
import time

class Kindle:
    @staticmethod
    def _command(command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        return proc.stdout.read()

    @staticmethod
    def display_image(im):
        if Kindle.on_kindle():
            im = im.transpose(Image.ROTATE_270)
            image_to_bytes_to_file(im, "/dev/fb0")
            Kindle.refresh_screen()
        else:
            im.show()

    def refresh_screen():
        Kindle._command("echo 1 > /sys/devices/platform/mxc_epdc_fb/mxc_epdc_update")

    @staticmethod
    def on_kindle():
        return 'kindle' in Kindle._command(['uname', '-a'])

    @staticmethod
    def battery_capacity():
        if Kindle.on_kindle():
            return int(Kindle._command(["cat", "/sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity"])[:-1])
        else:
            return random.randint(0, 99);

class FrameGenerator:
    resolution = (1024, 768)

    background_color = (255)
    foreground_color = (0)

    mainFont = ImageFont.truetype("./fonts/LiberationMono-Regular.ttf", 555)
    smallFont = ImageFont.truetype("./fonts/LiberationMono-Regular.ttf", 45)
    tinyFont = ImageFont.truetype("./fonts/LiberationMono-Regular.ttf", 25)

    def generate_waiting_image(self, time):
        mainText = "{: >2d}m".format(time).rjust(3)
        subText="Until the next Loop Bus arrives"
        subTextTwo="Get the app, http://fake.url/"

        im = Image.new('L', self.resolution, self.background_color)

        draw  =  ImageDraw.Draw(im)
        draw.text((10, 35), mainText, font=self.mainFont, fill=self.foreground_color)
        draw.text((10, 65), "___", font=self.mainFont, fill=self.foreground_color)
        draw.text((50, 630), subText, font=self.smallFont, fill=self.foreground_color)
        draw.text((50, 690), subTextTwo, font=self.tinyFont, fill=self.foreground_color)
        del draw

        return im

fb = FrameGenerator()

while True:
    im = fb.generate_waiting_image(Kindle.battery_capacity())
    Kindle.display_image(im)
    time.sleep(60)

