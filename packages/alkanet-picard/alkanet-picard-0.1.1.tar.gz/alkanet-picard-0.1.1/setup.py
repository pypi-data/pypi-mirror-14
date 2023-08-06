from setuptools import setup, find_packages

setup(name='alkanet-picard',
      version='0.1.1',
      description='Declarative Hyperparameter Optimization for Keras models',
      url='http://github.com/jakebian/picard',
      author='Jake Bian',
      author_email='jake@getalkanet.com',
      packages=find_packages(),
      install_requires=[
        'keras',
        'h5py'
      ],
      zip_safe=False)
