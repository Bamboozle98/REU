# REU
Collection of ML models and files relevant to research in the REU program at East Carolina University. 


All development was done on Windows 10 machines. Models were run in a miniconda enviornment and trained on a Desktop GEFORCE RTX 3070 TI. All models were run with the PyCharm IDE.

# Specifications for the Miniconda enviornment
Python==3.9  
Tensorflow==2.10  
cudatoolkit=11.2  
cudnn=8.1.0  
These version installations will be referenced in the miniconda setup instructions. 

# Instructions for Miniconda Setup
Before you do anything, you need the Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, and 2019. This download can be found at (https://visualstudio.microsoft.com/vs/community/). Note that you do not need any of the additional packages offered in the Visuall C++ Redistributable install, just install the barebones package. You need this redistributable because some software packages used in this setup use the C++ language. 

Download miniconda (Miniconda3), conda version 23.3.1 (latest as of 6/6/2023). Check your version with 'conda -V' within the 'Anaconda Prompt (miniconda3)' powershell. 
Open the miniconda powershell by searching in the windows search bar for 'Anaconda Prompt (miniconda3).'
Once open, input the following command to begin creating your python enviornment:
                              
                       conda create --name #### python==3.9
                      
where '####' represents a name that you can assign to the python enviornment you are creating. 
After your enviornment is created, run the following command to activate it within your powershell:

                       conda activate ####
                       
Once the enviornment is running, run the following command to install CUDA and the cuDNN tool into the enviornment:

                       conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
                       

Then you need to install TensorFlow with the following command:

                       pip install tensorflow==2.10
                       
You should now be all set to start coding within this enviorment and use python commands to refer tensorflow to your GPU as opposed to your CPU.
You can check to see if tensorflow recognizes your GPU with the following python script:

                       print(tf.config.list_physical_devices('GPU'))
                       
Which, if your setup worked, will print something like this:

                       [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
      
Output will vary depending on your hardware setup, but as long as it is printing a recognized device, you should be good. Note that the above to statements are directly from python script so you will either have to put them in .py file and run the file through the miniconda powershell, or run them directly in the miniconda powershell with 'python -c print(tf.config.list_physical_devices('GPU'))'.

Once you know that your GPU is recognized by TensorFlow, you can tell your script to use the GPU for certain calculations. For instance:

                      with tf.device('GPU:0'):
                          model.compile(optimizer=keras.optimizers.Adam(0.001),
                                        loss=tf.keras.losses.CategoricalCrossentropy(),
                                        metrics=[tf.keras.metrics.CategoricalAccuracy()])
                          model.fit(train_data, epochs=20, validation_data=test_data, batch_size=32, callbacks=callbacks)
                          
Every line within the 'with tf.device('GPU:0'):' command is being calculated by the GPU. 
Here is a link to a guide on setting up GPU support with TensorFlow.  
https://www.tensorflow.org/install/pip
