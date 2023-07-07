import re
import glob
import os

# This code was written as the framework for parsing through my database file directory to automatically scrape images.
# It iterates through the indexes 19 to end because I implemented this code after doing the first 20 directories one by
# one.
# This code was incorporated into the Google-Image_Scraper main.py file as well as the duplicate_image_obliterater.py
file_list = 'E:/My Data v.4/theropod/'

for fname in os.listdir(file_list)[20:]:
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        print(f[0])
        name = f[0]
        path = 'E:/My Data v.4/Scraped data(Post Manual Cleaning)/' + name
        os.mkdir(path)