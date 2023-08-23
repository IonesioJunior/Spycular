# setup.py
import os

from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension(
        "pynocchio.utils.uuid_gen",
        ["pynocchio/utils/uuid_gen.pyx"],
    ),
    Extension(
        "pynocchio.pointer.object_pointer",
        ["pynocchio/pointer/object_pointer.py"],
    ),
]

# gcc arguments hack: enable optimizations
os.environ["CFLAGS"] = "-O3"


setup(
    ext_modules=cythonize(extensions),
)
