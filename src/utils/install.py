import os
import subprocess
#######################################################################################     
def install_retinanet():
  subprocess.call('git clone https://github.com/fizyr/keras-retinanet.git'.split(' '))
  os.chdir('keras-retinanet')
  subprocess.call('pip install /content/keras-retinanet/'.split(' '))
  subprocess.call('python setup.py build_ext --inplace'.split(' '))

