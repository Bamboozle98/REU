# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable
import re
import glob

# The purpose of this file is to scrape images from the web in order to supplement my dataset. This code incorporates
# the file_string_parser.py to iterate through the majority of my file directory as opposed to manually one-by-one. The
# original web scraping file is available on github at https://github.com/ohyicong/Google-Image-Scraper
# This is not my original work and has been modified for this particular project.

file_list = 'E:/My Data v.4/theropod/'

for fname in os.listdir(file_list)[20:]:
    f = os.path.join(file_list, fname)
    if os.path.isdir(f):
        f = fname.split(' ', 1)
        name = f[0]


        def worker_thread(search_key):
            image_scraper = GoogleImageScraper(
                webdriver_path,
                image_path,
                search_key,
                number_of_images,
                headless,
                min_resolution,
                max_resolution,
                max_missed)
            image_urls = image_scraper.find_image_urls()
            image_scraper.save_images(image_urls, keep_filenames)

            #Release resources
            del image_scraper

        if __name__ == "__main__":
            #Define file path
            webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
            image_path = 'E:/My Data v.4/Scraped data(Post Manual Cleaning)/' + name + '/'

            #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
            search_keys = list(set([name + " skeleton", name + " skull", name + " fossil"]))

            #Parameters
            number_of_images = 100                # Desired number of images
            headless = True                     # True = No Chrome GUI
            min_resolution = (0, 0)             # Minimum desired image resolution
            max_resolution = (9999, 9999)       # Maximum desired image resolution
            max_missed = 10                     # Max number of failed images before exit
            number_of_workers = 1               # Number of "workers" used
            keep_filenames = False              # Keep original URL image filenames

            #Run each search_key in a separate thread
            #Automatically waits for all threads to finish
            #Removes duplicate strings from search_keys
            with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
                executor.map(worker_thread, search_keys)
