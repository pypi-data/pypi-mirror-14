from setuptools import setup

setup(name='tabfileio',
      version='0.2.0',
      description='Tabular file input/output in multiple formats',
      long_description=('This package is used to read and write numerical'
                        ' tabular data. It is made for handling data in'
                        ' columns with a header (a text identifier). Supported'
                        ' formats are text, zipped text, excel (xls and xlsx),'
                        ' python pickle, json, and HDF5.'),
      classifiers=[  # Classifier list:  https://pypi.python.org/pypi?:action=list_classifiers
                   "Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Topic :: Database",
                   "Topic :: Scientific/Engineering",
                   "Topic :: Scientific/Engineering :: Information Analysis",
                   "Topic :: Utilities",
                  ],
      url='https://github.com/sswan/tabfileio',
      author='Scot Swan',
      author_email='scot.swan@gmail.com',
      license='MIT',
      packages=['tabfileio',],
      install_requires=['numpy', 'xlrd', 'xlwt', 'openpyxl', 'h5py'],
      zip_safe=False)
