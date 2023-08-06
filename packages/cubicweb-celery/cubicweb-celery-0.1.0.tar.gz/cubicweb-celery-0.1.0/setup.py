import os
from glob import glob

from setuptools import setup

setup(
    name='cubicweb-celery',
    version='0.1.0',
    description='Celery integration with CubicWeb',
    author='Christophe de Vienne',
    author_email='christophe@unlish.com',
    packages=['cubicweb_celery'],
    install_requires=[
        'celery', 'cubicweb'
    ],
    data_files=[
        (os.path.join('share', 'cubicweb', 'cubes', 'celery'),
         glob('cubes/celery/*.py'))
    ])
