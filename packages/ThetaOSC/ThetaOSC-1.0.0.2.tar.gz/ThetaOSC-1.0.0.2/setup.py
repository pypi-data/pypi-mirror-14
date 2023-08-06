#!python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import os

ext_modules = [  Extension("generate_DF_to_ER_map", ["generate_DF_to_ER_map.pyx"]),
                 ]
ext_modules=cythonize(ext_modules)

setup(
    name = 'ThetaOSC',
    version='1.0.0.2',
    description="Library to control Richo Theta-S through WiFi with OSC API",
    author="Noboru Yamamoto",
    author_email="use a link in https://souran.kek.jp/kss/staffDetailInformation/view/1180",
    #language="c++", # this causes Cython to create C++ source
    ext_modules = ext_modules,
    py_modules=["ThetaOSC"],
)
