# Data Acquisition and Augmentation
Our data was extracted from the Fossil Image Dataset (FID) created and used by Liu et al., 2022 in their study 
[Automatic taxonomic identification based on the Fossil Image Dataset (>415,000 images) and deep convolutional neural networks](https://www.cambridge.org/core/journals/paleobiology/article/automatic-taxonomic-identification-based-on-the-fossil-image-dataset-415000-images-and-deep-convolutional-neural-networks/4863E2FDE20D6115415EE5FE232B9DCD). I will link the FID [here](https://zenodo.org/record/6333970).

The FID dataset is comprised of almost half a million images that were scraped from the web and organized into clades for classification by a neural network. In addition to their organization of clades, they also seemed to place each image into a genus within each clade. My goal for this project is to take the clade theropod and create a convolutional neural network (CNN) to see if it can classify theropod dinosaur fossil images into the genera provided in the dataset. Make note that I am not an expert or even novice paleontologist and therefore cannot validate the accuracy to which these fossil images were organized. My goal is to create a model that will classify the images from the FID using the class structure (directory structure) provided by the FID. 

# Dataset Version Control
For this project, I created a total of 5 different version of my dataset to train the models on. Every new version is meant to be an improvement on the previous for training purpose. The changes made to each iteration was either class removal, data cleaning, or data supplementation. 

## Version 1
Version 1 is the theropod folder from the FID database as it comes. No changes were made to this version.

## Version 2
Version 2 was an attempt to create version 3, however, for some reason the folder was corrupted and could not be used by the models. Version 3 is a copy of Version 2, but is not corrupted. 

## Version 3
Version 3 is Version 1 except I removed some folders (classes) from the theropod clade that I believed to be irrelevant to my goal. My modifications to the theropod folder in the FID are as follows:

-deleted the first 2 folders named with box characters. '╝¼┴·' '╩▐╜┼╤╟─┐'.  

-deleted folder 'aa_add'  

-deleted folder ‘Muraenosaurus skeleton’  

-deleted folder ‘Museum Spinosaurus skeleton’  

-deleted folder ‘Museum Tyrannosaur skeleton’  

-deleted folder ‘real Tyrannosaurus fossil’  

-deleted folder ‘Tyrannosaurus rex skeleton’  

-deleted folder ‘Tyrannosaurus skeleton’  

-In total, deleted 9 folders. Went from 20,622 total images to 18,631 total images. Went from 112 classes to 103 classes.  

## Version 4
Version 4 represents the largest change in the dataset in a single given step. It includes class removal, data supplementation, and data cleaning. To start, an image count was taken for every class. This paragraph represents a breif overview of the steps I took in modifying the data for Version 4. More detailed information of the changes can be found below. 

### 1. Class Removal:
   Any class that had below 50 images by default was removed. Classes with low image couunts and little data to supplement them would have a negative bias from the models trained on the data which could skew the results. Additionally, folders with absurdly high image counts and poor classification value would have a positive bias from the model and skew the results. One folder in particular was a 'problem child' for this project. The folder named 'Bing-saurischia' which encompassed any theropod image from the Bing search engine contained over ~8,000 images alone of the ~20,000 total. Most other folders contained somewhere between 50 and 200 images. Additionally, the 'Bing-saurischia' folder had images in it that belonged in other classes, thus models trained on the dataset would confuse the same theropod for two different classes. I believe this folder was created as a sort of miscelaneous dump for images the researchers couldn't or didn't want to classify by genus. They did not need to for the purposes of their research. Conversely, my research does require it. Therefore, I chose to remove the folder all together.
   
Below are the removed classes:
Moved 'Tyrannosaurus rex fossil into 'Tyrannosaurus fossil', renamed 'Tyrannosaurus fossil' to 'Tyrannosaurus skeleton'.
Removed the following classes due to low image count
Agrosaurus skeleton
Ajancingenia skeleton
Anserimimus skeleton
Avimimus skeleton
Bing-saurischia
Genyodectes skeleton
Hagryphus skeleton
Harpymimus skeleton
Ilokelesia skeleton
Khaan skeleton
Ligabueino skeleton
Muraenosaurus fossil
Piatnitzkysaurus skeleton
Sinovenator skeleton
Tianyuraptor skeleton
Xiaotingia skeleton
Xunmenglong skeleton
Zupaysaurus skeleton
   
### 2. Data Supplementation: 
Removing 'Bing-saurischia' created a new problem however, I had lost almost half of my entire dataset. I determined that I had to supplement my dataset. I found a google chrome image scraper and re-tooled it for my purposes, then scraped over ~15,000 images.
   
### 3. Data cleaning: 
I went through every image one-by-one and determined whether or not it belonged in that class. Afterwards, I copied all the images into the approriate folders of my theropod dataset. After attempting to run my new dataset, I realized the 'flow_from_directory' function I was using from the Tensorflow library did not work with certain file types that I had scraped from the web. I had to remove theses file types in order for the function to identify the actual amount of images in each folder. 

Moved 'Tyrannosaurus rex fossil into 'Tyrannosaurus fossil', renamed 'Tyrannosaurus fossil' to 'Tyrannosaurus skeleton'.
Removed the following classes due to low image count
Agrosaurus skeleton
Ajancingenia skeleton
Anserimimus skeleton
Avimimus skeleton
Genyodectes skeleton
Hagryphus skeleton
Harpymimus skeleton
Ilokelesia skeleton
Khaan skeleton
Ligabueino skeleton
Muraenosaurus fossil
Piatnitzkysaurus skeleton
Sinovenator skeleton
Tianyuraptor skeleton
Xiaotingia skeleton
Xunmenglong skeleton
Zupaysaurus skeleton


After I modified the data directory, I ran the 'data_split.py' file on my new modified theropod folder. This script split the available data into a training set, a validation set, and a testing set with the ratios 80%, 10%, and 10% respectively. These are the data files I reference for data generation within my models. For instance:

    tr_data = ImageDataGenerator()
    train_data = tr_data.flow_from_directory(directory="E:/My Data v.3/split_data/train",
                                             target_size=(224, 224))
                                                                 
is an example of how I load these datasets into my models.
