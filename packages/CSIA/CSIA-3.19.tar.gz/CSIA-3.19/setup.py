from distutils.core import setup
from setuptools import setup, find_packages

setup(name = 'CSIA',  
      version = '3.19',
      keywords = 'CRISPR Sequence Indel Analyze',
      description = 'CRISPR Sequence Indel Analyze', 
      long_description = 'After CRISPR experiment on DNA, sequencing target region and analyze indel frequency.',
      license = 'GPLv3',
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Programming Language :: Python :: 2.7',
      ],
      author = 'Yingxiang Li',  
      author_email = 'xlccalyx@gmail.com', 
      maintainer = 'Yingxiang Li',
      url = 'www.calyx.biz',
      download_url = 'http://www.calyx.biz/downloading--1997936733.html',
      packages = ['CSIA'],
      package_dir = {'CSIA': 'CSIA'},
      scripts = ['CSIA/CSIA'],
      package_data = {'CSIA': ['VarScan.v2.3.9.jar', 'example.input.tab']}
) 

