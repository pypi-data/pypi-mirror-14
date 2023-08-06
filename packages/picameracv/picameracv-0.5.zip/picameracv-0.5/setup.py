import os
from setuptools import setup


def read(fname):
    HERE = os.path.abspath(os.path.dirname(__file__))
    print HERE
    #return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "picameracv",
    version = "0.5",
    author = "geka",
    author_email = "geka.kud@gmail.com",
    description ="Project for picamera/webcamera image processing and pattern detections",
    license = "GNU General Public License (GPL)",
    keywords = "picamera image processing",
    url = "http://packages.python.org/picameracv",
    packages=['cameramodule', 'initializer'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],

    include_package_data=True,
    # relative to the vfclust directory
    package_data={
        'classifiers':[ 'haarcascade_eye.xml',
                        'haarcascade_frontalface_default.xml',
                        'haarCascadeRoad.xml'],
        'signtext':[]
    },
)
