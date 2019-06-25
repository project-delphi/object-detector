import urllib	
import subprocess	
PRETRAINED_MODEL = './snapshots/_pretrained_model.h5'	

 #### OPTION 1: DOWNLOAD INITIAL PRETRAINED MODEL FROM FIZYR ####	
URL_MODEL = 'https://github.com/fizyr/keras-retinanet/releases/download/0.5.0/resnet50_coco_best_v2.1.0.h5'	
urllib.request.urlretrieve(URL_MODEL, PRETRAINED_MODEL)	

 #### OPTION 2: DOWNLOAD CUSTOM PRETRAINED MODEL FROM GOOGLE DRIVE. CHANGE DRIVE_MODEL VALUE. USE THIS TO CONTINUE PREVIOUS TRAINING EPOCHS ####	
#drive.mount('/content/gdrive')	
#DRIVE_MODEL = '/content/gdrive/My Drive/Colab Notebooks/objdet_tensorflow_colab/resnet50_csv_10.h5'	
#shutil.copy(DRIVE_MODEL, PRETRAINED_MODEL)	

print('Downloaded pretrained model to ' + PRETRAINED_MODEL)	

cmd = 'keras_retinanet/bin/train.py --freeze-backbone --random-transform --weights ' + PRETRAINED_MODEL + ' --batch-size 8 --lr 1e-3  --steps 200 --epochs 25 csv annotations.csv classes.csv'	
subprocess.call(cmd)	

 #### OPTIONAL: EXPORT TRAINED MODEL TO DRIVE ####	
drive.mount('/content/gdrive')	
COLAB_MODEL = './snapshots/resnet50_csv_03.h5'	
DRIVE_DIR = '/content/gdrive/My Drive/sargassum/'	
shutil.copy(COLAB_MODEL, DRIVE_DIR) 