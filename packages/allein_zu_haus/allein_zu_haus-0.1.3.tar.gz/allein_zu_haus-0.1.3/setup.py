from setuptools import setup, Extension, Command
from distutils.command.build_ext import build_ext
import numpy.distutils.misc_util
import os
import os.path
import time
import glob
import sys
import shutil
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


_py3 = sys.version_info >= (3, 0)
_python_interpreter = 'python3' if _py3 else 'python'


class _TestCommand(Command):
    user_options = [
        ('which=', None, 'Specify the test to run.')
        ]

    def initialize_options(self):
        self.which = None

    def finalize_options(self):
        if self.which is None:
            self.which = ''

    def run(self):
        # TODO(AmiT)
        run_str = "%s -m unittest discover allein_zu_haus '*test.py'" % _python_interpreter
       	os.system(run_str)


_ext_modules = [
    Extension(
        '_callein_zu_haus',
        ['allein_zu_haus/_callein_zu_haus.pyx', 'allein_zu_haus/align.cpp'],
        language='c++',
        extra_compile_args=["-std=c++11"],
        extra_link_args=["-std=c++11"])]


setup(
    name='allein_zu_haus',
    version='0.1.3',
    author='Tali Raveh-Sadka, Ami Tavory, and Shahar Azulay',
    author_email='atavory@gmail.com',
    packages=[
        'allein_zu_haus'],
    package_data={
    },
    include_package_data=True,
    scripts=[
    ],
    ext_modules=cythonize(_ext_modules),
    license='License :: OSI Approved :: BSD License',
    description='Needleman-Wunsch quality-aware sequence alignmenti, primarily for use with a full aligner like GEM.',
    long_description=open('README.rst').read(),
    requires=['numpy', 'cython'],
    zip_safe=False,
    cmdclass={
        'test': _TestCommand},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'])




