import os

import keras
import tensorflow as tf
import pandas

from keras_retinanet import models

def get_session():
  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  return tf.Session(config=config)
  
def configure_keras():
  keras.backend.tensorflow_backend.set_session(get_session())
########################################################################################

def model_object(import_from_drive, args):
  import os
  drive_path, classes_path, threshold_score = args
  if import_from_drive:
    model_path = drive_path
  else:
    sorted_list_dir = sorted(os.listdir('snapshots'))
    model_path = os.path.join('snapshots', sorted_list_dir, reverse=True)[0]
  # load retinanet model
  model = models.load_model(model_path, backbone_name='resnet50')
  model = models.convert_model(model)
  # load label to names mapping for visualization purposes
  labels_to_names = pandas.read_csv(classes_path, header=None).T.loc[0].to_dict()
  return (model, labels_to_names, threshold_score)

########################################################################################


def img_inference(img_path, model_object):
  import keras
  from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
  from keras_retinanet.utils.visualization import draw_box, draw_caption
  from keras_retinanet.utils.colors import label_color
  # import miscellaneous modules
  import matplotlib.pyplot as plt
  import cv2
  import os
  import numpy as np
  import time
  print('Running inference on: ' + img_path)
  model, labels_to_names, THRESHOLD_SCORE = model_object
  image = read_image_bgr(img_path)
  # copy to draw on
  draw = image.copy()
  draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
  # preprocess image for network
  image = preprocess_image(image)
  image, scale = resize_image(image)
  # process image
  start = time.time()
  boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
  print("processing time: ", time.time() - start)
  # correct for image scale
  boxes /= scale
  # visualize detections
  for box, score, label in zip(boxes[0], scores[0], labels[0]):
      # scores are sorted so we can break
      if score < THRESHOLD_SCORE:
          break
      color = [255,0,0] # prefer RED ##label_color(label)      
      b = box.astype(int)
      draw_box(draw, b, color,thickness=7) # heavy border boxes
      caption = "{} {:.3f}".format(labels_to_names[label], score)
      draw_caption(draw, b, caption)
  plt.figure(figsize=(10, 10))
  plt.axis('off')
  plt.imshow(draw)
  plt.show()