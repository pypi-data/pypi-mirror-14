from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy


extensions = [
    Extension("bhtsne_wrapper",
        ['bhtsne_wrapper.pyx', 'src/tsne.cpp', 'src/sptree.cpp'],
        include_dirs=[numpy.get_include(), 'src'],
        extra_link_args=['-Wl,-framework', '-Wl,Accelerate', '-lcblas'],
        extra_compile_flags=['-I/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers'],
        language='c++'
        )
]

setup(
    name="bhtsne",
    version="0.1.0",
    description='Python module for Barnes-Hut implementation of t-SNE (Cython)',
    url='https://github.com/dominiek/python-bhtsne',
    ext_modules=cythonize(extensions),
    install_requires=['numpy', 'cython']
)
