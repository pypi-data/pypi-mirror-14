try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name='antk',
      version=0.1,
      description='Automated Neural-graph Toolkit: A Tensorflow wrapper for '
                  'common deep learning tasks and rapid development of new'
                  'models.',
      url='http://aarontuor.xyz',
      author='Aaron Tuor',
      author_email='tuora@students.wwu.edu',
      license='none',
      packages=['ANT/datascripts'],
      scripts=['ANT/datascripts/datatest.py', 'ANT/datascripts/normalize.py',
               'ANT/antdocs.py'],
      zip_safe=False,
      install_requires=['scipy', 'numpy', 'tensorflow'],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'],
    keywords=[
        'Deep Learning',
        'Neural Networks',
        'TensorFlow',
        'Machine Learning',
        'Western Washington University'])