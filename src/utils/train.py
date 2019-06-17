import urllib
import shutil
from google.colab import drive
########################################################################################
def import_model(drive_model_flag,dest, src):
  if drive_model_flag:
    drive.mount('/content/gdrive')
    src = '/content/gdrive/My Drive/sargassum/resnet50_csv_03.h5'
    shutil.copy(src, dest)
  else:
    src = 'https://github.com/fizyr/keras-retinanet/releases/download/0.5.0/resnet50_coco_best_v2.1.0.h5'
    urllib.request.urlretrieve(src, dest)
  print('Downloaded pretrained model to: ' + dest)
#########################################################################################
def export_model(dest, src):
  drive.mount('/content/gdrive')
  shutil.copy(src, dest)
