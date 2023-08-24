# setup.py
import os

from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension(
        "spycular.utils.uuid_gen",
        ["spycular/utils/uuid_gen.pyx"],
    ),
]

# gcc arguments hack: enable optimizations
os.environ["CFLAGS"] = "-O3"


setup(
    ext_modules=cythonize(extensions),
)
