from distutils.core import setup, Extension
import numpy.distutils.misc_util

c_ext = Extension('_ucrdtw', ['ucrdtw/src/_ucrdtw.c', 'ucrdtw/src/ucrdtw.c'])

setup(
    name='ucrdtw',
    packages = ['ucrdtw'],
    version='0.103',
    url='https://pypi.python.org/pypi/pip',
    maintainer='m3at',
    maintainer_email='paul@alpacadb.com',
    description='Fast Dynamic Time Warping, O(n log n) ',
    long_description='Based on the following paper: http://www.cs.ucr.edu/~eamonn/SIGKDD_trillion.pdf',
    license='MIT',
    keywords='Dynamic Time Wraping',
    install_requires=['numpy'],
    ext_modules=[c_ext],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
