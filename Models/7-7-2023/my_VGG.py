import tensorflow as tf
import keras
import io
import scipy
from keras import layers, optimizers, losses, metrics, applications
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential, regularizers
from keras.utils import to_categorical
from keras.optimizers import SGD, Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.applications import VGG19, Xception, VGG16
from keras.layers import Input, Flatten, Dense, BatchNormalization, Activation, Dropout, GlobalAveragePooling2D, \
    MaxPooling2D, RandomFlip, RandomZoom, RandomRotation

print(tf.config.list_physical_devices('GPU'))  # Make sure TensorFlow can see our GPU.

# Begin data generation and loading.
tr_data = ImageDataGenerator()
train_data = tr_data.flow_from_directory(directory="E:/My Data v.5/split_data/train",
                                         target_size=(224, 224),
                                         interpolation='bilinear')
ts_data = ImageDataGenerator()
test_data = ts_data.flow_from_directory(directory="E:/My Data v.5/split_data/val",
                                        target_size=(224, 224),
                                        interpolation='bilinear')

# Load the VGG16 architecture from ImageNet.
vgg = keras.applications.VGG16(
    weights="imagenet",  # Load weights pre-trained on ImageNet.
    input_shape=(224, 224, 3),
    include_top=False,
    classifier_activation='softmax'
)  # Do not include the ImageNet classifier at the top.

vgg.trainable = False  # Freeze all VGG16 layers.

# Augment dataset to further test the model's ability to classify.
data_augmentation = Sequential(
    [RandomFlip("horizontal"),
     RandomRotation(0.1),
     RandomZoom(0.1)]
)

# Add on the last few layers that we will train independently before unfreezing the model.
x = Flatten()(vgg.output)
x = Dense(512, activation='relu')(x)  # A FC layer with 512 nodes and the ReLu activation function.
prediction = Dense(50, activation='softmax')(x)  # Another FC layer with 103 nodes in reference to our # of classes.
model = keras.Model(inputs=vgg.input, outputs=prediction)  # Assign our model to a variable to run.

model.summary()  # Print a summary of our model layers and parameters.

callbacks = [EarlyStopping(monitor='categorical_accuracy', patience=5, verbose=0)]

with tf.device('GPU:0'):  # Instructing TensorFlow to execute the next 4 lines of code with our GPU.
    model.compile(optimizer=keras.optimizers.Adam(0.001),  # Compile our model with additional parameters.
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=[tf.keras.metrics.CategoricalAccuracy()])
    model.fit(train_data, epochs=20, validation_data=test_data, batch_size=32, callbacks=callbacks)  # Begin training.

for layer in model.layers[:5]:  # Unfreeze the top 5 layers in our model.
    layer.trainable = True
model.summary()  # Print an updated summary of our model which includes the 5 layers we just unfroze.

with tf.device('GPU:0'):  # Instructing TensorFlow to execute the next 8 lines of code with our GPU.
    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),  # Low learning rate
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=[tf.keras.metrics.CategoricalAccuracy()]
    )

    epochs = 10
    model.fit(train_data, epochs=epochs, validation_data=test_data, batch_size=32, callbacks=callbacks)
    # Train model again with newly unfrozen layers.

    model.save_weights(
        "E:/My_Models/my_weights/" + str(model.history['val_categorical_accuracy'][-1]) + "_" + str(epochs) + ".h5")
