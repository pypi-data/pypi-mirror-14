from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

ext_modules=[
    Extension("potions.solver", ["potions/solver.pyx"], language='c++'),       
    Extension("potions.sparse_solver", ["potions/sparse_solver.pyx"], language='c++'),       
]

setup(
  name = 'potions',
  ext_modules = ext_modules,
  include_dirs=[numpy.get_include()],
  packages=['potions'],
)

