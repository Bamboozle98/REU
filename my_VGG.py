import tensorflow as tf
import keras
from keras import layers, optimizers, losses, metrics, applications
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential, regularizers
from keras.utils import to_categorical
from keras.optimizers import SGD, Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.applications import VGG19, Xception, VGG16
from keras.layers import Input, Flatten, Dense, BatchNormalization, Activation, Dropout, GlobalAveragePooling2D, \
    MaxPooling2D, RandomFlip, RandomZoom, RandomRotation


tr_data = ImageDataGenerator()
train_data = tr_data.flow_from_directory(directory="E:/My Data v.1/split_data/train", target_size=(224, 224))
ts_data = ImageDataGenerator()
test_data = ts_data.flow_from_directory(directory="E:/My Data v.1/split_data/val", target_size=(224, 224))


vgg = keras.applications.VGG16(
    weights="imagenet",  # Load weights pre-trained on ImageNet.
    input_shape=(224, 224, 3),
    include_top=False,
    classifier_activation='softmax'
)  # Do not include the ImageNet classifier at the top.
vgg.trainable = False

data_augmentation = Sequential(
    [RandomFlip("horizontal"),
     RandomRotation(0.1),
     RandomZoom(0.1)]
)

x = Flatten()(vgg.output)
x = Dense(512, activation='relu')(x)
prediction = Dense(112, activation='softmax')(x)
model = keras.Model(inputs=vgg.input, outputs=prediction)

model.summary()

callbacks = [EarlyStopping(monitor='val_accuracy', patience=5, verbose=0)]

model.compile(optimizer=keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])
model.fit(train_data, epochs=20, validation_data=test_data, batch_size=32, callbacks=callbacks)


# Unfreeze the base_model. Note that it keeps running in inference mode
# since we passed `training=False` when calling it. This means that
# the batchnorm layers will not update their batch statistics.
# This prevents the batchnorm layers from undoing all the training
# we've done so far.
for layer in model.layers[:5]:
    layer.trainable = True
model.summary()

model.compile(
    optimizer=keras.optimizers.Adam(1e-5),  # Low learning rate
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=[tf.keras.metrics.CategoricalAccuracy()]
)

epochs = 10
model.fit(train_data, epochs=epochs, validation_data=test_data, batch_size=32, callbacks=callbacks)
