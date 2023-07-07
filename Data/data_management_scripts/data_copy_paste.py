import os
import shutil

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

