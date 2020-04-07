import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2 #to install it -> !pip install opencv-python
from tensorflow import keras
from collections import defaultdict
import collections
from shutil import copy
from shutil import copytree, rmtree
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import tensorflow.keras.backend as K
from tensorflow.keras import regularizers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2
from tensorflow.keras import models
from pathlib import Path
from tensorflow.keras.optimizers import SGD

# This function slipts the dataset into train and test folders:
def prepare_data(filepath, src,dest):
    classes_images = defaultdict(list)
    with open(filepath, 'r') as txt:
        paths = [read.strip() for read in txt.readlines()]
        for p in paths:
            food = p.split('/')
            classes_images[food[0]].append(food[1] + '.jpg')

    for food in classes_images.keys():
        print("\nCopying images into ",food)
        if not os.path.exists(os.path.join(dest,food)):
            os.makedirs(os.path.join(dest,food))
        for i in classes_images[food]:
            copy(os.path.join(src,food,i), os.path.join(dest,food,i))
    print("Copying Done!")

# Prepare train dataset by copying images from food-images/images_type to food-images/train using the file train.txt
print("Creating train data...")
prepare_data('food-images/image_salads/train.txt', 'food-images/image_salads', 'food-images/image_salads/train')

# Prepare test data by copying images from food-images/images_type to food-images/test using the file test.txt
print("Creating test data...")
prepare_data('food-images/image_salads/test.txt', 'food-images/image_salads', 'food-images/image_salads/test')


#MODEL CLASSIFICATION

#To know where the last dimension goes:
K.image_data_format()

def model_classification(NUM_CLASSES, train_data_folder_path, validation_data_folder_path, filepath_name, csv_train_name, model_name_save):
    #Clearing the session removes all the nodes left over from previous models, freeing memory and preventing slowdown.
    K.clear_session()


    #Defining number of clases, num of pixels, batch_size-> dataset divided in blocks to train
    #Epochs->num of times the model runs the same dataset
    IMG_ROWS, IMG_COLS = 128, 128
    BATCH_SIZE = 16
    EPOCHS = 20


    #Folder to take train and test data into:
    train_data_folder = train_data_folder_path
    validation_data_folder = validation_data_folder_path


    #defining the total number of train and validation images:
    num_train_samples = 33750
    num_validation_samples = 11250

    train_datagenerator = ImageDataGenerator(rescale=1. / 255,
                                             shear_range=0.2,
                                             zoom_range=0.2,
                                             horizontal_flip=True)


    test_datagenerator = ImageDataGenerator(rescale=1. / 255)


    train_generator = train_datagenerator.flow_from_directory(train_data_folder,
                                                             target_size=(IMG_ROWS, IMG_COLS),
                                                             batch_size=BATCH_SIZE,
                                                             class_mode='categorical')


    test_generator = test_datagenerator.flow_from_directory(validation_data_folder,
                                                           target_size=(IMG_ROWS, IMG_COLS),
                                                           batch_size=BATCH_SIZE,
                                                           class_mode='categorical')


    # create the base pre-trained model:
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(IMG_ROWS, IMG_COLS, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.2)(x) #use to reduce overfiting


    predictions = Dense(NUM_CLASSES, kernel_regularizer=regularizers.l2(0.005), activation='softmax')(x)


    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
    checkpointer = ModelCheckpoint(filepath=filepath_name, verbose=1, save_best_only=True)
    csv_logger = CSVLogger(csv_train_name)

    history = model.fit_generator(train_generator,
                        steps_per_epoch = num_train_samples // BATCH_SIZE,
                        validation_data=test_generator,
                        validation_steps=num_validation_samples // BATCH_SIZE,
                        epochs=EPOCHS,
                        verbose=1,
                        callbacks=[csv_logger, checkpointer])

    model.save(model_name_save)

#Training plates model
model_classification(45, 'food-images/image_plates/train', 'food-images/image_plates/test', 'best_model_45plates.hdf5', 'traning_total_45plates.log', 'model_trained_45plates.hdf5')

#Training salads model
model_classification(5, 'food-images/image_salads/train', 'food-images/image_salads/test', 'best_model_5salads.hdf5', 'traning_total_5salads.log', 'model_trained_5salads.hdf5')

#Training deserts model
model_classification(9, 'food-images/image_desert/train', 'food-images/image_desert/test', 'best_model_9deserts.hdf5', 'traning_total_9deserts.log', 'model_trained_9deserts.hdf5')