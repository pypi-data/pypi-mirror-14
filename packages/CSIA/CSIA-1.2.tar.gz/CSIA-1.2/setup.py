from setuptools import setup, find_packages

setup(name = 'CSIA',  
      version = '1.2',
      keywords = 'CRISPR Sequence Indel Analyze',
      description = 'CRISPR Sequence Indel Analyze', 
      long_description = 'After CRISPR experiment on DNA, sequencing target region and analyze indel frequency.',
      license = 'MIT',
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2.7',
      ],
      author = 'Yingxiang Li',  
      author_email = 'xlccalyx@gmail.com', 
      maintainer = 'Yingxiang Li',
      url = 'www.calyx.biz',
      download_url = 'http://www.calyx.biz/uploads/2/1/9/2/21925892/csia-1.0.tar.gz',
      packages = ['CSIA'],
      package_dir = {'CSIA': 'CSIA'},
      scripts = ['CSIA/CSIA.py'],
      package_data = {'CSIA': ['VarScan.v2.3.9.jar']}
) 

