from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
import platform

link_args = ['-O2']
if platform.system() == 'Darwin':
    link_args = ['-Wl,-framework', '-Wl,Accelerate', '-lcblas']

extensions = [
    Extension("bhtsne_wrapper",
        ['bhtsne_wrapper.pyx', 'src/tsne.cpp', 'src/sptree.cpp'],
        include_dirs=[numpy.get_include(), 'src'],
        extra_link_args=link_args,
        extra_compile_flags=['-I/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers'],
        language='c++'
        )
]

setup(
    name="bhtsne",
    version="0.1.2",
    description='Python module for Barnes-Hut implementation of t-SNE (Cython)',
    url='https://github.com/dominiek/python-bhtsne',
    ext_modules=cythonize(extensions),
    install_requires=['numpy', 'cython']
)
