# Data Acquisition and Augmentation
Our data was extracted from the Fossil Image Dataset (FID) created and used by Liu et al., 2022 in their study 
[Automatic taxonomic identification based on the Fossil Image Dataset (>415,000 images) and deep convolutional neural networks](https://www.cambridge.org/core/journals/paleobiology/article/automatic-taxonomic-identification-based-on-the-fossil-image-dataset-415000-images-and-deep-convolutional-neural-networks/4863E2FDE20D6115415EE5FE232B9DCD).

Their dataset is comprised of almost half a million images that they scraped from the web and organized into clades for classification by their neural network. In addition to their organization of clades, they also seemed to place each image into a genus within each clade. My goal for this project is to take the clade theropod and create a convolutional neural network (CNN) to see if it can classify theropod dinosaur fossil images into the geneses provided in the dataset. Make note that I am not an expert or even novice paleontologist and therefore cannot validate the accuracy to which these fossil images were organized. My goal is to create a model that will classify the images from the FID using the class structure (directory structure) provided by the FID. That being said, I removed some folders (classes) from the theropod clade that I believed to be irrelevant to my goal. My modifications to the theropod folder in the FID are as follows:

-deleted the first 2 folders named with box characters. '╝¼┴·' '╩▐╜┼╤╟─┐'.  

-deleted folder 'aa_add'  

-deleted folder ‘Muraenosaurus skeleton’  

-deleted folder ‘Museum Spinosaurus skeleton’  

-deleted folder ‘Museum Tyrannosaur skeleton’  

-deleted folder ‘real Tyrannosaurus fossil’  

-deleted folder ‘Tyrannosaurus rex skeleton’  

-deleted folder ‘Tyrannosaurus skeleton’  

-In total, deleted 9 folders. Went from 20,622 total images to 18,631 total images. Went from 112 classes to 103 classes.  

After I modified the data directory, I ran the 'data_split.py' file on my new modified theropod folder. This script split the available data into a training set, a validation set, and a testing set with the ratios 80%, 10%, and 10% respectively. These are the data files I reference for data generation within my models. For instance:

    tr_data = ImageDataGenerator()
    train_data = tr_data.flow_from_directory(directory="E:/My Data v.3/split_data/train",
                                             target_size=(224, 224))
                                                                 
is an example of how I load these datasets into my models. I will link the FID [here](https://zenodo.org/record/6333970).
