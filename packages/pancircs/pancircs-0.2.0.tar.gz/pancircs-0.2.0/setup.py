# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:29:55 2016

Setup file for the biosigpy package.

Ing.,Mgr. (MSc.) Jan Cimbálník
Biomedical engineering
International Clinical Research Center
St. Anne's University Hospital in Brno
Czech Republic
&
Mayo systems electrophysiology lab
Mayo Clinic
200 1st St SW
Rochester, MN
United States
"""

from setuptools import setup

setup(name='pancircs',
      version='0.2.0',
      install_requires=['pandas','matplotlib'],
      description='Package for circualar visualization of data in pandas',
      url='http://github.com/cimbi/pancircs',
      author='Jan Cimbalnik',
      author_email='jan.cimbalnik@fnusa.cz, jan.cimbalnik@mayo.edu',
      license='BSD 3.0',
      packages=['pancircs'],
      keywords='pandas circle visualization',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Visualization'],
      zip_safe=False)