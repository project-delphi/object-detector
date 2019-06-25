import argparse

parser = argparse.ArgumentParser(description='inference program to predict using trained model to new files')
parser.add_argument('--trained_model', type=str, default='data/processed/training/unzipped', 
help='path of trained_model')
parser.add_argument('--classes', type=str, default='data/processed/training/unzipped', 
help='path of classes csv file')
parser.add_argument('--threshold', type=int, default='data/processed/training/unzipped', 
help='threshold to classify at')
parser.add_argument('--inpath', type=str, default='data/processed/training/unzipped', 
help='directory of new image data to be inferred on')
parser.add_argument('--outpath', type=str, default='data/processed/training/unzipped', 
help='directory to save files from inference output')
args = parser.parse_args()

# doesn't work, but intention is here
import inference
import subprocess

"""
 install data and model files
!pip install keras_retinanet

inference.configure_keras()
args = (args.trained_model, args.classes, args.threshold, args.inpath)
model_object = inference.model_object(import_from_drive = True, args = args)
list(map(in, inference.img_inference))
subprocess.call(F'mv {inpath} {outpath}')
# run inference

"""