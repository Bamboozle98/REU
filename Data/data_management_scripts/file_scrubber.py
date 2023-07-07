import os
# This code was used to remove all of the file types in my dataset that were not png, jpeg, or jpg. The flow_from_directory 
# function would not identify all images otherwise. This code incorporates the file_string_parser script to iterate through
# all folders in my dataset. 
file_list = 'E:/My Data v.4/theropod/'
count = 0

for fname in os.listdir(file_list):
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        name = f[0]
        print(name)

        dir_name = "E:/My Data v.4/theropod/" + name + " skeleton/"
        test = os.listdir(dir_name)

        for image in test:
            if not image.endswith(".jpg") and not image.endswith(".jpeg") and not image.endswith(".png"):
                print(dir_name + image)
                count += 1
                os.remove(os.path.join(dir_name, image))
print(count)

#        for item in test:
#            if item.endswith(".webp") or item.endswith(".gif") or item.endswith(".mpo") or item.endswith(".bpm") or item.endswith("."):
   #             print(item)
         #       os.remove(os.path.join(dir_name, item))
