import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import tensorflow_datasets as tfds
from concurrent_plugin import concurrent_core
import os
import sys


print("Arguments if any: ", sys.argv)

print('Environment## 1' , os.environ)
#Load model and label dictionary
model_df = concurrent_core.list('/Users/jitendra/Kaggle/data/Bird-Species/bird_species/model/', "model_input")

print('Environment## 2' , os.environ)
model_files = concurrent_core.get_local_paths(model_df)

print('Environment## 3' , os.environ)
for ff in model_files:
    print(ff)
    if 'EfficientNetB4' in ff:
        model = keras.models.load_model(ff)
    elif 'class_dict' in ff:
        class_labels_df = pd.read_csv(ff)
        
class_labels_dict = {row['class']: row['class_index'] for i, row in class_labels_df.iterrows()}


print(class_labels_dict['CROW'], class_labels_dict['BLUE HERON'], class_labels_dict['PINK ROBIN'])


#Preprocess images
def preprocess_image(img_path):
    image = tf.io.read_file(img_path)
    image1 = tf.io.decode_jpeg(image, channels=3)
    image2 = tf.image.resize(image1, [112, 112])
    return image2


#Make Image Dataset
test_df = concurrent_core.list("/Users/jitendra/Kaggle/data/Bird-Species/bird_species/test/", "data_input")

data_files = concurrent_core.get_local_paths(test_df)

if not data_files:
    print("No data files nothing to do")
    exit(0)

print(data_files[1:10])


path_ds = tf.data.Dataset.from_tensor_slices(data_files)

##Preprocessing dataset
image_ds = path_ds.map(preprocess_image)


#Make label dataset
all_image_labels = [class_labels_dict[os.path.basename(os.path.dirname(img_path)).replace('_', ' ')] for img_path in data_files]

print(all_image_labels[1:10])

label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))


##Combine image and label dataset
image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

image_label_ds = image_label_ds.batch(16)

## Iterator
ds_numpy_iter = tfds.as_numpy(image_label_ds)

correct_labels = 0
num_predictions = 0
batch_num=0
for i in ds_numpy_iter:
    if batch_num % 5 == 0:
        print('Predicting batch {}'.format(batch_num))
    batch_num += 1
    img, label = i
    predictions = model.predict(img)
    predicted_classes = np.argmax(predictions, axis=1)
    
    correct_labels += np.sum(label == predicted_classes)
    num_predictions += predicted_classes.shape[0]

accuracy = float(correct_labels)/num_predictions

print("Number of Predictions = {},\nCorrect Predictions = {},\nAccuracy = {}".format(num_predictions, correct_labels, accuracy))

