from os import chdir
from subprocess import run

def install_retinanet():
  run('git clone https://github.com/fizyr/keras-retinanet.git'.split(' '))
  chdir('keras-retinanet')
  run('pip install /content/keras-retinanet/'.split(' '))
  run('python setup.py build_ext --inplace'.split(' '))


