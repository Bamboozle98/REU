import re
import glob
import os

# This code was used to automatically create all of the directories needed to store my scraped data. 
# This code incorporates the file_string_parser script to iterate through all folders in my dataset. 
file_list = 'E:/My Data v.4/theropod/'

for fname in os.listdir(file_list)[20:]:
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        print(f[0])
        name = f[0]
        path = 'E:/My Data v.4/Scraped data(Post Manual Cleaning)/' + name
        os.mkdir(path)
