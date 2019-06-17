import subprocess
import gdown
from google.colab import drive

####################################################

def ingest_data(mount_drive_flag, drive_id,dataset_dir='dataset', output = 'cropped_images.zip'):
  if mount_drive_flag:
    drive.mount('/content/gdrive')
    return None
  subprocess.call(F'mkdir {dataset_dir}'.split(' '))
  subprocess.call(F'cd {dataset_dir}'.split(' '))
  url =  F'https://drive.google.com/uc?id={drive_id}'
  gdown.download(url, output, quiet=False)
  subprocess.call('cd ..', shell=True)
  
####################################################

import os 
import csv
import xml.etree.ElementTree as ET

def process_root(root, dataset_dir, annotations = [], classes = set([])):
  for elem in root:
    if elem.tag == 'filename':
      file_name = os.path.join(dataset_dir, elem.text)
    if elem.tag == 'object':
      obj_name = None
      coords = []
      for subelem in elem:
        if subelem.tag == 'name':
          obj_name = subelem.text
        if subelem.tag == 'bndbox':
          for subsubelem in subelem:
            coords.append(subsubelem.text)
      item = [file_name] + coords + [obj_name]
      annotations.append(item)
      classes.add(obj_name)
      return (annotations, classes)

def xml2csv(dataset_dir = 'dataset', annotations_file = 'annotations.csv', classes_file = 'classes.csv'):
  for xml_file in [f for f in os.listdir(dataset_dir) if (f.endswith(".xml") and not f.startswith('._')) ]:
    tree = ET.parse(os.path.join(dataset_dir, xml_file))
    root = tree.getroot()
    annotations, classes = process_root(root, dataset_dir)

  with open(annotations_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(annotations)

  with open(classes_file, 'w') as f:
    for i, line in enumerate(classes):
      f.write('{},{}\n'.format(line,i))
#######################################################################################      
import os
import subprocess
def install_retinanet():
  subprocess.call('git clone https://github.com/fizyr/keras-retinanet.git'.split(' '))
  os.chdir('keras-retinanet')
  subprocess.call('pip install /content/keras-retinanet/'.split(' '))
  subprocess.call('python setup.py build_ext --inplace'.split(' '))
 ######################################################################################
import subprocess
def format_data():
  subprocess.call('rm -rf /content/keras-retinanet/dataset'.split(' '))
  subprocess.call('mkdir /content/keras-retinanet/dataset'.split(' '))
  subprocess.call(['unzip', '-q', '-j', '/content/gdrive/My Drive/sargassum/cropped_images.zip',
                 '-d', '/content/keras-retinanet/dataset/'])
  subprocess.call('rm -rf dataset/._*'.split(' '),shell=True)
  xml2csv()
########################################################################################
import urllib
import shutil
def import_pretrained_model(drive_model_flag,dest, src):
#### OPTION 1: DOWNLOAD INITIAL PRETRAINED MODEL FROM FIZYR ####
  if drive_model_flag:
    drive.mount('/content/gdrive')
    src = '/content/gdrive/My Drive/sargassum/resnet50_csv_03.h5'
    shutil.copy(src, dest)
  else:
    src = 'https://github.com/fizyr/keras-retinanet/releases/download/0.5.0/resnet50_coco_best_v2.1.0.h5'
    urllib.request.urlretrieve(src, dest)
  print('Downloaded pretrained model to: ' + dest)
#########################################################################################
import shutil
from google.colab import drive
def export_trained_model(dest, src):
  drive.mount('/content/gdrive')
  shutil.copy(src, dest)
#########################################################################################


def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)


# set the modified tf session as backend in keras
def configure_keras():
  import keras
  from keras_retinanet import models
  from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
  from keras_retinanet.utils.visualization import draw_box, draw_caption
  from keras_retinanet.utils.colors import label_color
  # import miscellaneous modules
  import matplotlib.pyplot as plt
  import cv2
  import os
  import numpy as np
  import time
  # set tf backend to allow memory to grow, instead of claiming everything
  import tensorflow as tf
  keras.backend.tensorflow_backend.set_session(get_session())
########################################################################################
import os
import pandas

def model_object(import_from_drive, args):
  drive_path, classes_path, threshold_score = args
  if import_from_drive:
    model_path = drive_path
  else: 
    model_path = os.path.join('snapshots', sorted(os.listdir('snapshots'), reverse=True)[0])
  # load retinanet model
  model = models.load_model(model_path, backbone_name='resnet50')
  model = models.convert_model(model)
  # load label to names mapping for visualization purposes
  labels_to_names = pandas.read_csv(classes_path, header=None).T.loc[0].to_dict()
  return (model, labels_to_names, threshold_score)

########################################################################################

def img_inference(img_path, model_object):
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
################################################################################