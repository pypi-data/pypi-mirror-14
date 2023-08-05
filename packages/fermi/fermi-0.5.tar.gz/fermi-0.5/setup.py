from setuptools import setup
from distutils.core import Extension




try:
    from Cython.Build import cythonize
    core_src=['fermi/src/intcore.pyx',]
    core_c_ext=Extension('fermi/src/intcore',sources=core_src,extra_link_args=['-fopenmp',],extra_compile_args=['-fopenmp',])
    ext_modules=cythonize(core_c_ext)
except:
    ext_modules=[]

setup(
            name='fermi',
            version='0.5',
            url='https://github.com/iogiul/FERMI',
            author='Giuliano Iorio',
            author_email='giuliano.iorio@unibo.it',
            package_dir={'fermi/src/':''},
            packages=['fermi','fermi/src'],
            install_requires=['numpy>=1.9','scipy>=0.16'],
            ext_modules=ext_modules
    )
