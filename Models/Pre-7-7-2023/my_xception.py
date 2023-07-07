import tensorflow as tf
import keras
from keras import layers, optimizers, losses, metrics, applications
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential, regularizers
from keras.utils import to_categorical
from keras.optimizers import SGD, Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.applications import VGG19, Xception
from keras.layers import Input, Flatten, Dense, BatchNormalization, Activation, Dropout, GlobalAveragePooling2D, \
    MaxPooling2D, RandomFlip, RandomZoom, RandomRotation


tr_data = ImageDataGenerator()
train_data = tr_data.flow_from_directory(directory="E:/My Data v.2/split_data/train", target_size=(299, 299))
ts_data = ImageDataGenerator()
test_data = ts_data.flow_from_directory(directory="E:/My Data v.2/split_data/val", target_size=(299, 299))


base_model = keras.applications.Xception(
    weights="imagenet",  # Load weights pre-trained on ImageNet.
    input_shape=(299, 299, 3),
    include_top=False,
    classifier_activation='softmax'
)  # Do not include the ImageNet classifier at the top.
base_model.trainable = False

data_augmentation = Sequential(
    [RandomFlip("horizontal"),
     RandomRotation(0.1),
     RandomZoom(0.1)]
)

inputs = keras.Input(shape=(299, 299, 3))
# The base model contains batchnorm layers. We want to keep them in inference mode
# when we unfreeze the base model for fine-tuning, so we make sure that the
# base_model is running in inference mode here.
x = data_augmentation(inputs)
x = tf.keras.applications.xception.preprocess_input(x)

# Pre-trained Xception weights requires that input be scaled
# from (0, 255) to a range of (-1., +1.), the rescaling layer
# outputs: `(inputs * scale) + offset`
# Pre-trained Xception weights requires that input be scaled
# from (0, 255) to a range of (-1., +1.), the rescaling layer
# outputs: `(inputs * scale) + offset`
scale_layer = keras.layers.Rescaling(scale=1 / 127.5, offset=-1)
x = scale_layer(x)

x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
# x = keras.layers.Dropout(0.2)(x)  # Regularize with dropout
# x = keras.layers.Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
outputs = keras.layers.Dense(103, activation='softmax')(x)
model = keras.Model(inputs, outputs)

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
base_model.trainable = True
model.summary()

model.compile(
    optimizer=keras.optimizers.Adam(1e-5),  # Low learning rate
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=[tf.keras.metrics.CategoricalAccuracy()]
)

epochs = 10
model.fit(train_data, epochs=epochs, validation_data=test_data, batch_size=32, callbacks=callbacks)
