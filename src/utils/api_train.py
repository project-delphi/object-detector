import argparse

parser = argparse.ArgumentParser()
parser.add_argument('training_data')
parser.add_argument('hyperparameters')
args = parser.parse_args()

"""
 install repo and dependencies
!git clone https://github.com/project-delphi/object-detector.git
!mv object-detector/src/utils .

import utils.install as install 
install.install_retinanet()
DRIVE_ID = '1xzBJWcjtBDCg10kwjpwZ85t_oXD0a7kt'
mount_drive_flag = True
import utils.data as data
data.ingest(mount_drive_flag, DRIVE_ID)
# ALTERNATIVE OPTION download via shareable link with mount_drive_flag=False
data.format()
# MODEL_PATH = os.path.join('snapshots', sorted(os.listdir('snapshots'), reverse=True)[0])
MODEL_PATH = '/content/keras-retinanet/snapshots/_pretrained_model.h5'
import utils.train as train
train.import_model(drive_model_flag=False, dest=MODEL_PATH, src=None)
# run training
#!keras_retinanet/bin/train.py --freeze-backbone --random-transform --weights {MODEL_PATH} --batch-size 8 --lr 1e-3  --steps 3 --epochs 1 csv annotations.csv classes.csv    
dest='/content/gdrive/My Drive/sargassum/'
src='./snapshots/resnet50_csv_10.h5'
import utils.train as train
train.export_model(dest, src)
"""