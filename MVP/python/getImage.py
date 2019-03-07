#!/usr/bin/env python

from picamera import PiCamera
import time
# Save as CouchDB attachment
# import saveImage

#Use this line for MVP 2.0
dir = '/home/pi/MVP/pictures_R/'

#Create file name with timestamp
ts=time.strftime("%Y-%m-%d-%H%M%S")
image_name=ts+'_R.jpg'
file_name=dir +image_name
#print(file_name)
camera = PiCamera()

# Adjust brightness and ISO for lighting
#camera.contrast=50
#camera.brightness=70
#camera.saturation=50
#camera.ISO=100

# Capture an image
camera.start_preview()
time.sleep(2)
camera.capture(file_name)
camera.stop_preview()

#saveImage.save(ts, image_name, file_name, 'Raspberry', 'Left')
