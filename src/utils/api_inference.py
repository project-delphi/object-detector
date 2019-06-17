import argparse

parser = argparse.ArgumentParser()
parser.add_argument('trained_model')
parser.add_argument('classes')
parser.add_argument('threshold')
parser.add_argument('inpath')
parser.add_argument('outpath')
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