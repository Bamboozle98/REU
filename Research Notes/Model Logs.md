# 6/19/2023 10:00 AM
## VGG16
### Parameters for model import    
    weights="imagenet",
    input_shape=(224, 224, 3),
    include_top=False,
    classifier_activation='softmax'
### Layers added to the top of the model before training
    x = Dense(512, activation='relu')(x)  
    prediction = Dense(103, activation='softmax')(x)
### Hyperparameters
    Epochs for last two layers only = 20
    Adam optimizer for last two layers only = 0.001
    Epochs for last two layers and top 5 layers of VGG16 = 10
    Adam optimizer for last two layers and top 5 layers of VGG16 = 1e-5
    Batch size = 32
### Results
    
## Xception
### Parameters for model import    
    weights="imagenet",
    input_shape=(299, 299, 3),
    include_top=False,
    classifier_activation='softmax'
### Layers added to the top of the model before training
    scale_layer = keras.layers.Rescaling(scale=1 / 127.5, offset=-1)
    x = scale_layer(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = keras.layers.Dense(103, activation='softmax')(x)
### Hyperparameters
    Epochs for last two layers only = 20
    Adam optimizer for last two layers only = 0.001
    Epochs for last two layers and all Xception layers = 10
    Adam optimizer for last two layers and all Xception layers = 1e-5
    Batch size = 32
### Results
    
## Bilinear VGG16
### Parameters for both model imports
    tensor_input = keras.layers.Input(shape=[150, 150, 3])
    input_tensor=tensor_input,
    include_top=False,
    weights='imagenet'
### Layers added to the top of the model before training
    x = keras.layers.Dense(units=103,
                           kernel_regularizer=keras.regularizers.l2(0.0),
                           kernel_initializer=initializer)(x)

    tensor_prediction = keras.layers.Activation("softmax")(x)

    model_bilinear = keras.models.Model(inputs=[tensor_input],
                                        outputs=[tensor_prediction])
### Hyperparameters
    Optimizer for frozen round of training
    sgd = keras.optimizers.SGD(lr=1.0, decay=0.0, momentum=0.9)
    
    epochs for frozen round of training = 20
    workers = 3,
    verbose = 1
    epochs for second unfrozen of training = 30
    
    optimizer for unfrozen round of training
    sgd = keras.optimizers.SGD(lr=1e-3, decay=1e-9, momentum=0.9)
### Results
    
