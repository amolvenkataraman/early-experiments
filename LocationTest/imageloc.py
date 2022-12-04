import os
import glob
import argparse
import datetime
import json
import exifread
from PIL import Image, ExifTags, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
from GPSPhoto import gpsphoto

#ALBUMS = ['C:/Users/Admin/Desktop/DCIM/Camera/']
ALBUMS = ['H:/DCIM/Camera/']
TOTAL = 0
COORDS = []

for album in ALBUMS:
    try:
        print(f"{album}/")
        files = os.listdir(f"{album}/")
        TOTAL += len(files)
        for file in files:
            try:
                fp = f"{album}/{file}"
                gpsdata = gpsphoto.getGPSData(fp)
                COORDS.append([gpsdata['Latitude'], gpsdata['Longitude']])
            except: pass
    except FileNotFoundError: pass

with open('gps.json', 'w+') as f:
    json.dump(COORDS, f) 