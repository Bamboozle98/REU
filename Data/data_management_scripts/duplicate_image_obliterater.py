import hashlib
import os

file_list = 'E:/My Data v.4/theropod/'

# The purpose of this code is to remove duplicate images within the file directory Theropod. It does not always get
# every duplicate image, but does average about 40-50 images removed in my experience. I recommend using this in
# conjunction with manual data cleaning. This code incorporates the file_string_parser.py file to iterate through most
# of my dataset directory.

for fname in os.listdir(file_list):
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        name = f[0]

        hashes = set()
        directory = "E:/My Data v.4/theropod/" + name + " skeleton"
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            digest = hashlib.sha1(open(path,'rb').read()).digest()
            if digest not in hashes:
                hashes.add(digest)
            else:
                os.remove(path)