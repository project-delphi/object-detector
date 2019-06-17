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
      


def img_inference(img_path, model, THRESHOLD_SCORE = 0.6):
  image = read_image_bgr(img_infer)

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