# The following libraries need to be installed:
# Author: Howard Webb
# Date: 2/12/2018
# This program selects pictures within a date range, then selects one per day and converts them to a GIF

import os
from datetime import datetime, timedelta
from PIL import Image

def getPics(dir, type, start_date, end_date, test=False):
    '''Select last picture of each day since start of trial
           Args:
               dir: directory where pictures are located
               type: file format (usually jpg)
               start_date: start of the trial
               end_date: end time (usually current time)
               test:
           Returns:
               pics: array of file names
           Raises:
               None
    '''               
    if test:
        print("Get Pics from " + dir + " " + start_date + " to " + end_date)
        
    prior_day=0
    pics=[]
    for file in sorted(os.listdir(dir)):
        if file.endswith(type):
            dt=file.split('_')
#            if test:
#                print file, dt

            if dt[0] > start_date and dt[0] < end_date:
                # get one image per day
                day=dt[0].split('-')
                now=day[2]
#            print now, prior_day
                if now!=prior_day:
                    if test:
                        print(file + " " +  str(os.stat(dir + file).st_size))
                    prior_day = now
                    pics.append(dir+file)
    return pics

def pic_to_img(pics, test=False):
    '''Open pictures as images
           Args:
               pics: array of file names
               test:
           Returns:
               img: array of image structures
           Raises:
               None
    '''  
    if test:
        print("Open pictures as images")
    images=[]
    for p in pics:
        images.append(Image.open(p))
    return images        
        

def resize_images(images, size, test=False):
    '''Reduce image size for better processing and display
           Args:
               images: array if image data
               size: list of desired image size
               test:
           Returns:
               img: array of resized image structures
           Raises:
               None
    '''  

    if test:
        print("Resize: " + str(size))
    out = []
    for img in images:
        rimg = img.resize(size)
        out.append(rimg)
    return out

def get_start_date(test=False):
    '''Start date is the beginning of a trial - set in env.py
        If env.py is missing, or data is invalid, then default to 4 weeks ago
           Args:
               None:
           Returns:
               start_date
           Raises:
               None
    '''  
    start_date = None
    tmp_date = str(datetime.now() - timedelta(days=30))
    try:
        from env import env
        start_date=env["trials"][0]["start_date"]
        if start_date < tmp_date:
            start_date = tmp_date
    except Exception as e:
        if test:
            print(e)
        start_date  = tmp_date
    if test:
        print("Start Date: " + start_date)
    return start_date

def make_gif(images, test=False):
    '''Convert set of images to a GIF and saves to file
           Args:
               images: array of image data
               test:
           Returns:
               None:
           Raises:
               None
    '''  
    
    output_file = "/home/pi/MVP/web/plant.gif"
    duration = 0.2
    images[0].save(output_file, format='GIF', append_images=images[1:], save_all=True, duration=100, loop=0)
    if test:
        print("GIF Output: " + output_file)
        
def main(test=False):
    '''Main controller of processing
           Args:
               test:
           Returns:
               None:
           Raises:
               None
    '''  
    
    # Variables to control source and output
    start_date = get_start_date(test)
    end_date=str(datetime.now())
    # Source of images
    dir="/home/pi/MVP/pictures/"
    # Image type to select
    type=".jpg"
    # Resize the image to 640x480 (resizing will keep ratio with one dimension specified)
    size=[640, 480]
    # Output file name (will be in the python directory with this code)
    png_name="plant.gif"
    pics=getPics(dir, type, start_date, end_date, test)
    images = pic_to_img(pics, test)
    pics = resize_images(images, size, test)
    make_gif(pics, test)

if __name__=="__main__":
    main()    
