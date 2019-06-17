import subprocess
import gdown
from google.colab import drive

####################################################
def ingest(mount_drive_flag, drive_id,dataset_dir='dataset', output = 'cropped_images.zip'):
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
import subprocess

def format():
  subprocess.call('rm -rf /content/keras-retinanet/dataset'.split(' '))
  subprocess.call('mkdir /content/keras-retinanet/dataset'.split(' '))
  subprocess.call(['unzip', '-q', '-j', '/content/gdrive/My Drive/sargassum/cropped_images.zip',
                 '-d', '/content/keras-retinanet/dataset/'])
  subprocess.call('rm -rf dataset/._*'.split(' '),shell=True)
  xml2csv()  