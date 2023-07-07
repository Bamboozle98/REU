import os
import shutil

# This code was used to copy all of the cleaned images scraped from the web and paste them into the approriate 
# folders containing my dataset. 
# This code incorporates the file_string_parser script to iterate through all folders in my dataset. 

file_list = 'E:/My Data v.4/theropod/'

for fname in os.listdir(file_list)[20:]:
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        name = f[0]
        print(name)

        src = r"E:/My Data v.4/Scraped data(Post Manual Cleaning)/" + name + '/'
        dest = r'E:/My Data v.4/theropod/' + name + ' skeleton/'

        files = os.listdir(src)
        for file in files:
            files_2 = os.listdir(src + file)
            #print('\n' + file)
            for image in files_2:
                #print(image)
                print(src + file + image)
                shutil.copy2(src + file + '/' + image, dest + image)

