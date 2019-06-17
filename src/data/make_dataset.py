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
  for xml_file in [f for f in os.listdir(dataset_dir) if f.endswith(".xml") ]:
    tree = ET.parse(os.path.join(dataset_dir, xml_file))
    root = tree.getroot()
    annotations, classes = process_root(root, dataset_dir)

  with open(annotations_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(annotations)

  with open(classes_file, 'w') as f:
    for i, line in enumerate(classes):
      f.write('{},{}\n'.format(line,i))
