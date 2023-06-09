# Data Acquisition and Augmentation
Our data was extracted from the Fossil Image Dataset (FID) created and used by Liu et al., 2022 in their study 
[Automatic taxonomic identification based on the Fossil Image Dataset (>415,000 images) and deep convolutional neural networks](https://www.cambridge.org/core/journals/paleobiology/article/automatic-taxonomic-identification-based-on-the-fossil-image-dataset-415000-images-and-deep-convolutional-neural-networks/4863E2FDE20D6115415EE5FE232B9DCD). I will link the FID [here](https://zenodo.org/record/6333970).

The FID dataset is comprised of almost half a million images that were scraped from the web and organized into clades for classification by a neural network. In addition to their organization of clades, they also seemed to place each image into a genus within each clade. My goal for this project is to take the clade theropod and create a convolutional neural network (CNN) to see if it can classify theropod dinosaur fossil images into the genera provided in the dataset. Make note that I am not an expert or even novice paleontologist and therefore cannot validate the accuracy to which these fossil images were organized. My goal is to create a model that will classify the images from the FID using the class structure (directory structure) provided by the FID. 

After I modified any given version of my data, I ran the 'data_split.py' file on my new modified theropod folder. This script split the available data into a training set, a validation set, and a testing set with the ratios 80%, 10%, and 10% respectively. These are the data files I reference for data generation within my models. For instance:

    tr_data = ImageDataGenerator()
    train_data = tr_data.flow_from_directory(directory="E:/My Data v.3/split_data/train",
                                             target_size=(224, 224))
                                                                 
is an example of how I load these datasets into my models.


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

-Moved 'Tyrannosaurus rex fossil into 'Tyrannosaurus fossil', renamed 'Tyrannosaurus fossil' to 'Tyrannosaurus skeleton'.

-Removed the following classes due to low image count

-Agrosaurus skeleton

-Ajancingenia skeleton

-Anserimimus skeleton

-Avimimus skeleton

-Bing-saurischia

-Genyodectes skeleton

-Hagryphus skeleton

-Harpymimus skeleton

-Ilokelesia skeleton

-Khaan skeleton

-Ligabueino skeleton

-Muraenosaurus fossil

-Piatnitzkysaurus skeleton

-Sinovenator skeleton

-Tianyuraptor skeleton

-Xiaotingia skeleton

-Xunmenglong skeleton

-Zupaysaurus skeleton
   
### 2. Data Supplementation: 
Removing 'Bing-saurischia' created a new problem however, I had lost almost half of my entire dataset. I determined that I had to supplement my dataset with more images. I found a google chrome image scraper and re-tooled it for my purposes, then scraped over ~15,000 images. The scraper I used can be found the 'data_scraper' directory in this repository. Please read the 'scraper_README' which clarifies the origin of the scraper and what changes I made to it. Using the scraper, I scraped google for images related to every genus with these keywords, _name_ fossil, _name_ skeleton, and _name_ skull where 'name' refers to a particular genus in my dataset. For example 'Dilophosaurus fossil', 'Dilophosaurus skelton', and 'Dilophosaurus skull'. Each keyword had a limit of 100 images, however, it was rare that the scraper found 100 images for any search. These images were stored in a seperate folder organized by genus name which were created using the 'directory_creation.py' file. Over 15,000 images were scraped in total. 
   
### 3. Data cleaning: 
I went through every image one-by-one and determined whether or not it belonged in that class. As mentioned before, I am not an expert or novice paleontologist. I struggle to identify the distinctions between Tarbosaurus and Tyrannosaurus based on close-up images of their skulls. That being said, the google image scraper would frequently provide images that were obviously incorrect. For instance, finding a sauropod in the spinosaurus folder. These obvious errors I felt comfortable rectifying. Additionally, for every genus, I would use google to determine what holotypes of each genus existed which would tell me what fossils we had of each genus, how much of a full reconstruction we had, and if the genus was valid. This process helped me with the genera that I had a harder time identifying myself. Afterwards, I copied all the images into the approriate folders of my theropod dataset. After attempting to run my new dataset, I realized the 'flow_from_directory' function I was using from the Tensorflow library did not work with certain file types that I had scraped from the web. Subsequently, the model would generate less predictions than there were files in my test folder. Those file types included .gif, .mbp, .mpo, and extensionless files. I had to remove theses file types with the 'file_scrubber.py' file in order for the function to identify the actual amount of images in each folder and generate the approriate amount of predictions. Once the data was fully clean, I copied the scraped images into the actual dataset using the 'data_copy_paste.py' file. This concluded the changes to Version 4 of my dataset.

Total image and class count after image supplementation and copy obliteration is 16,458 across 81 classes.

## Version 5
Version 5 is Version 4 with certain folders removed. While cleaning the data in Version 4, I took notes on which classes I thought may be ill-suited for model classification. The reasons I used for determining if a class was ill-suited included the class sharing many images with another class, the class having a low image count post supplementation, the class representing a dubious genus, or if I was too unsure about whether the images in a class actually belonged to that genus.  

Below are the classes I removed from Version 4:

Caudipteryx 

Coelurus 

Conchoraptor 

Dromiceiomimus 

Erlikosaurus 

Falcarius 

Fukuiraptor  

Halszkaraptor  

Jinfengopteryx 

Juravenator 

Mapusaurus 

Marshosaurus 

Megaraptor 

Metriacanthosaurus 

Pelelcanimimus 

Procertosaurus 

Protarchaeopteryx 

Qianzhousaurus 

Rahonavis 

Rajasaurus 

Rugops 

Saurophaganx 

Sauronithoides 

Scipionyx 

Siamotyrannus 

Sinocalliopteryx 

Troodon 

Velocisaurus 

Xuanhanosaurus 

Zhenyuanlong 

Zhuchengtyrannus 

Post class removal, there are 11,620 Files, 50 Folders
The reasoning for why I removed certain classes and kept others can be found in the 'Data Class Changes' file in the 'Research Notes' Directory.
