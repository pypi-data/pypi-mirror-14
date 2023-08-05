import numpy
from distutils.core import setup
from setuptools import find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import os
from os import path

def get_omp_flags():
    """Returns openmp flags if OpenMP is available.

    Implementation based on https://bitbucket.org/pysph/pysph
    """
    omp_compile_flags, omp_link_flags = ['-fopenmp'], ['-fopenmp']

    env_var = os.environ.get('USE_OPENMP', '')
    if env_var.lower() in ['0', 'false', 'n']:
        print("-"*70)
        print "OpenMP disabled. Enable using 'USE_OPENMP'"
        print("-"*70)
        return [], [], False

    from textwrap import dedent
    try:
        from Cython.Distutils import Extension
        from pyximport import pyxbuild
    except ImportError:
        print("Unable to import Cython, disabling OpenMP for now.")
        return [], [], False
    from distutils.errors import CompileError, LinkError
    import shutil
    import tempfile
    test_code = dedent("""
    from cython.parallel import parallel, prange, threadid
    cimport openmp
    def n_threads():
        with nogil, parallel():
            openmp.omp_get_num_threads()
    """)
    tmp_dir = tempfile.mkdtemp()
    fname = path.join(tmp_dir, 'check_omp.pyx')
    with open(fname, 'w') as fp:
        fp.write(test_code)
    extension = Extension(
        name='check_omp', sources=[fname],
        extra_compile_args=omp_compile_flags,
        extra_link_args=omp_link_flags,
    )
    has_omp = True
    try:
        mod = pyxbuild.pyx_to_dll(fname, extension, pyxbuild_dir=tmp_dir)
        print("-"*70)
        print("Using OpenMP.")
        print("-"*70)
    except CompileError:
        print("*"*70)
        print("Unable to compile OpenMP code. Not using OpenMP.")
        print("*"*70)
        has_omp = False
    except LinkError:
        print("*"*70)
        print("Unable to link OpenMP code. Not using OpenMP.")
        print("*"*70)
        has_omp = False
    finally:
        shutil.rmtree(tmp_dir)

    if has_omp:
        return omp_compile_flags, omp_link_flags, True
    else:
        return [], [], False

requires = ["cython", "numpy", "pyevtk"]

ext_modules = []

ext_modules += [
        Extension(
            "pyspace.planet",
            ["pyspace/planet.pyx"],
            include_dirs = [numpy.get_include()]
            )
        ]

omp_compile_flags, omp_link_flags, use_omp = get_omp_flags()

ext_modules += [
        Extension(
            "pyspace.simulator",
            ["pyspace/simulator.pyx", "src/pyspace.cpp"],
            include_dirs = ["src", numpy.get_include()],
            extra_compile_args = omp_compile_flags,
            extra_link_args = omp_link_flags
            )
        ]

ext_modules = cythonize(ext_modules)

setup(
        name="PySpace",
        author="PySpace developers",
        author_email="adityapb1546@gmail.com",
        description="A toolbox for galactic simulations.",
        url = "https://github.com/adityapb/pyspace",
        long_description = open('README.rst').read(),
        version="0.0.2",
        install_requires=requires,
        packages=find_packages(),
        ext_modules = ext_modules
    )

