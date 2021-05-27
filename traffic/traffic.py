import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    dim = (IMG_WIDTH, IMG_HEIGHT)
    os.chdir(data_dir)
    directory = os.getcwd()
    #looping through folder
    for dirpath, dirnames, filenames in os.walk(directory):             #os.walk returns all files in directories recursively
        for filename in [f for f in filenames if f.endswith(".ppm")]:   #only choose the files with ".ppm" extension
            files = os.path.join(dirpath, filename)                     #combine the name of the file with the directory path, to get the absolute path
            img = cv2.imread(files)                                     #cv2 module image opening
            resized = cv2.resize(img, dsize=dim)                              #resize to the desirable dimensions
            images.append(resized)                                      #appending to the images list
            label = os.path.basename(os.path.dirname(files))            #os.path.dirname(files) returns the whole path, without the file name. os.path.basename returns the top directory.
            labels.append(str(label))
    
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    #create a neural network 
    model = tf.keras.models.Sequential([

            #Convolutional layer. The first value is the number of filters. Each filter acts on the size (second number) = (3,3) kernel.
            #Using relu activation (for real output, rather than binary 1 or 0)
            #input shape indicates the image dimension: 30x30 pixel, 3 colour channel (RGB).
            #Optionally, the batch size can be set in the input_shape. (first digit, if four variables are given).
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

            #Max-pooling layer, using 2x2 pool size. This reduces the size of the image while preserving the most important information
            #returns the largest value of each 2x2 pixel
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

            #Flatten units. This turns a 2D image to a 1D list
            tf.keras.layers.Flatten(),

            #Add a hidden layer with dropout. Dropout prevents overfitting, by dropping out some neurons.
            tf.keras.layers.Dense(256, activation="relu"),              #The hidden layer contains 512 nodes
            tf.keras.layers.Dropout(0.2),                               #Drop out 0.4 of the nodes

            #Output layer
            #number of output nodes = NUM_CATEGORIES.
            tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")     #softmax activation returns probability distribution on the number of output nodes, indicating the probability of each node
    ])

    #train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
