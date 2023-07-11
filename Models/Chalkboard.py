import tensorflow as tf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl
import cv2
import time
import PIL
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from keras.initializers import glorot_normal
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
   tf.config.experimental.set_memory_growth(physical_devices[0], True)
from matplotlib import pyplot
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

"""
Calculates dot product of x[0] and x[1] for mini_batch 

Assuming both have same size and shape

@param
x -> [ (size_minibatch, total_pixels, size_filter), (size_minibatch, total_pixels, size_filter) ]

"""
def dot_product(x):

    return keras.backend.batch_dot(x[0], x[1], axes=[1,1]) / x[0].get_shape().as_list()[1]

"""
Calculate signed square root

@param
x -> a tensor

"""

def signed_sqrt(x):

    return keras.backend.sign(x) * keras.backend.sqrt(keras.backend.abs(x) + 1e-9)

"""
Calculate L2-norm

@param
x -> a tensor

"""

def L2_norm(x, axis=-1):

    return keras.backend.l2_normalize(x, axis=axis)


'''

    Take outputs of last layer of VGG and load it into Lambda layer which calculates outer product.

    Here both bi-linear branches have same shape.

    z -> output shape tuple
    x -> outpur og VGG tensor
    y -> copy of x as we modify x, we use x, y for outer product.

'''


def build_model():
   tensor_input = keras.layers.Input(shape=[150, 150, 3])

   #   load pre-trained model
   tensor_input = keras.layers.Input(shape=[150, 150, 3])

   model_detector = keras.applications.vgg16.VGG16(
      input_tensor=tensor_input,
      include_top=False,
      weights='imagenet')

   model_detector2 = keras.applications.vgg16.VGG16(
      input_tensor=tensor_input,
      include_top=False,
      weights='imagenet')

   model_detector2 = keras.models.Sequential(layers=model_detector2.layers)

   for i, layer in enumerate(model_detector2.layers):
      layer._name = layer.name + "_second"

   model2 = keras.models.Model(inputs=[tensor_input], outputs=[model_detector2.layers[-1].output])

   x = model_detector.layers[17].output
   z = model_detector.layers[17].output_shape
   y = model2.layers[17].output

   print(model_detector.summary())

   print(model2.summary())
   #   rehape to (batch_size, total_pixels, filter_size)
   x = keras.layers.Reshape([z[1] * z[2], z[-1]])(x)

   y = keras.layers.Reshape([z[1] * z[2], z[-1]])(y)

   #   outer products of x, y
   x = keras.layers.Lambda(dot_product)([x, y])

   #   rehape to (batch_size, filter_size_vgg_last_layer*filter_vgg_last_layer)
   x = keras.layers.Reshape([z[-1] * z[-1]])(x)

   #   signed_sqrt
   x = keras.layers.Lambda(signed_sqrt)(x)

   #   L2_norm
   x = keras.layers.Lambda(L2_norm)(x)

   #   FC-Layer

   initializer = tf.keras.initializers.GlorotNormal()

   x = keras.layers.Dense(units=81,
                          kernel_regularizer=keras.regularizers.l2(0.0),
                          kernel_initializer=initializer)(x)

   tensor_prediction = keras.layers.Activation("softmax")(x)

   model_bilinear = keras.models.Model(inputs=[tensor_input],
                                       outputs=[tensor_prediction])

   #   Freeze VGG layers
   for layer in model_detector.layers:
      layer.trainable = False

   sgd = keras.optimizers.SGD(lr=1.0,
                              decay=0.0,
                              momentum=0.9)

   model_bilinear.compile(loss="categorical_crossentropy",
                          optimizer=sgd,
                          metrics=["categorical_accuracy"])

   model_bilinear.summary()

   return model_bilinear

model = build_model()


def train_model(epochs):
   hist = model.fit_generator(
      train_generator,
      epochs=epochs,
      validation_data=val_generator,
      workers=3,
      verbose=1
   )

   model.save_weights(
       "E:/My_Models/my_weights/" + str(hist.history['val_categorical_accuracy'][-1]) + "_" + str(epochs) + ".h5")

   return hist


train_datagen = image.ImageDataGenerator(
   rotation_range=40,
   width_shift_range=0.2,
   height_shift_range=0.2,
   fill_mode='nearest',
   rescale=1. / 255,
   shear_range=0.2,
   zoom_range=0.2,
   horizontal_flip=True)
test_datagen = image.ImageDataGenerator(rescale=1. / 255)
train_generator = train_datagen.flow_from_directory(
   "E:/My Data v.4/split_data/train",
   target_size=(150, 150),
   color_mode="rgb",
   batch_size=32,
   subset='training',
   class_mode='categorical')
val_generator = test_datagen.flow_from_directory(
   "E:/My Data v.4/split_data/val",
   target_size=(150, 150),
   color_mode="rgb",
   batch_size=32,
   subset='training',
   class_mode='categorical')
test_generator = test_datagen.flow_from_directory(
   "E:/My Data v.4/split_data/test",
   target_size=(150, 150),
   color_mode="rgb",
   shuffle=False,
   class_mode=None,
   batch_size=1)

hist =train_model(epochs=30)

for layer in model.layers:
    layer.trainable = True

sgd = keras.optimizers.SGD(lr=1e-3, decay=1e-9, momentum=0.9)

model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["categorical_accuracy"])
hist =train_model(epochs=50)

model.save('E:/My_Models/model_saves/')

model2 = keras.models.load_model('E:/My_Models/model_saves/')
preds = model2.predict_generator(test_generator, verbose=1)

preds_cls_idx = preds.argmax(axis=-1)

idx_to_cls = {v: k for k, v in train_generator.class_indices.items()}
preds_cls = np.vectorize(idx_to_cls.get)(preds_cls_idx)

true_lables = []
true_lables_upc_idx_map = {}
true_lables_img = {}
upc_list = os.listdir('E:/My Data v.5/split_data/test/')
idx = 0
for upc in upc_list:
    img_folder = 'E:/My Data v.5/split_data/test/' + upc +'/'
    img_list = os.listdir(img_folder)
    for img in img_list:
        true_lables.append(upc)
        true_lables_upc_idx_map[idx] = upc
        true_lables_img[idx] = img
        idx += 1
len(true_lables)

wrong_predicted = []
count = 0
for idx in range(0, len(preds_cls)):
    if preds_cls[idx] != true_lables[idx]:
        wrong_predicted.append(idx)
    else:
        count += 1

len(wrong_predicted)

accuracy = count/len(preds_cls)

wrong_pred_upc = set()
for label in wrong_predicted:
    wrong_pred_upc.add(true_lables_upc_idx_map[label])
len(wrong_pred_upc), len(wrong_predicted)

images_pred_wrong = []
for label in wrong_predicted:
    images_pred_wrong.append(true_lables_img[label])
len(images_pred_wrong)

for i in range(0 ,len(images_pred_wrong)):
    img ='E:/My Data v.5/split_data/test/' + true_lables_upc_idx_map[wrong_predicted[i]] + '/' + images_pred_wrong[i]
    print(img, preds_cls[i])

from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score
f1 = f1_score(true_lables, preds_cls, average='weighted')
precision = precision_score(true_lables, preds_cls, average='weighted')
recall  = recall_score(true_lables, preds_cls, average='weighted')
accuracy = accuracy_score(true_lables, preds_cls)
print("f1 :", f1)
print("precision :", precision)
print("recall :", recall)
print("accuracy :", accuracy)
