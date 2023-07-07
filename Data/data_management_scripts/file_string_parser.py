import re
import glob
import os

# This code was written as the framework for parsing through my database file directory to automatically scrape images.
# It iterates through the indexes 19 to end because I implemented this code after doing the first 20 directories one by
# one.
# This code was incorporated into the Google-Image_Scraper main.py, the duplicate_image_obliterater.py, the directory_creation.py,
# and the file_scrubber.py
file_list = 'E:/My Data v.4/theropod/'

for fname in os.listdir(file_list)[19:]:
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        print(f[0])
