#!/usr/bin/env python
"""Setup script for plastid. This is *fairly* boilerplate EXCEPT:

    1. `sdist`, `build_ext`, `install`, and `develop` commands are wrapped
       to add a "--recythonize" flag, which causes Cython to regenerate
       ".c" files from ".pyx" files before the commands are run.

    2.  These commands *also* invoke Cython if the ".c" files cannot be found.

    3. a `recythonize` command class was also created to do this, and only this

    4. a `clean` command class was added to wipe old ".c" files

    5. Separately, if the package is being installed on readthedocs.org,
       it only installs absolutely necessary build dependencies, which are
       numpy and pysam.
"""
__author__ = "Joshua Griffin Dunn"

import os
import sys
import glob
from collections import Iterable
from setuptools import setup, find_packages, Extension, Command
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.sdist import sdist
from setuptools.command.develop import develop


PYSAM_VER_NUM = (0,8,4)
NUMPY_VER_NUM = (1,9,0)

NUMPY_VERSION  = "numpy>=%s.%s.%s" % NUMPY_VER_NUM
SCIPY_VERSION  = "scipy>=0.15.1"
CYTHON_VERSION = "cython>=0.22"
PYSAM_VERSION  = "pysam>=%s.%s.%s" % PYSAM_VER_NUM

# require python >= 2.7 (for 2.x) or >= 3.3 (for 3.x branch)
version_message = "plastid requires Python >= 2.7 or >= 3.3. Aborting installation."
ver = sys.version_info
if ver < (2,7) or ver[0] == 3 and ver[1] < 3:
    raise RuntimeError(version_message)


def version_tuple(inp):
    return  tuple([int(X) for X in inp.split(".")])


# at present, setup/build can't proceed without numpy & Pysam
# adding these to setup_requires and/or install_requires doesn't work,
# because they are needed before them.
try:
    import numpy
    numpyver = version_tuple(numpy.__version__)
    if numpyver < NUMPY_VER_NUM:
        raise ImportError()

    import pysam
    pysamver = version_tuple(pysam.__version__)
    if pysamver < PYSAM_VER_NUM:
        raise ImportError()

    import Cython

except ImportError:
    print("""
    
*** IMPORTANT INSTALLATION INFORMATION ***

plastid setup requires %s, %s, and %s to be preinstalled. Please
install these via pip, and retry:

    $ pip install --upgrade numpy pysam cython
    $ pip install plastid

To see which versions you have installed:

    $ pip list | grep -E "(Cython|pysam|numpy)+"



""" % (NUMPY_VERSION,PYSAM_VERSION,CYTHON_VERSION))
    sys.exit(1)


#===============================================================================
# Simple stuff
#===============================================================================

with open("README.rst") as f:
    long_description = f.read()

plastid_version = "0.4.5"  #plastid.__version__ 
setup_requires = [NUMPY_VERSION,PYSAM_VERSION,CYTHON_VERSION]
packages = find_packages()


def get_scripts():
    """Detect command-line scripts automatically

    Returns
    -------
    list
        list of strings describing command-line scripts
    """
    binscripts = [X.replace(".py","") for X in filter(lambda x: x.endswith(".py") and \
                                                                "__init__" not in x,
                                                      os.listdir(os.path.join("plastid","bin")))]
    return ["%s = plastid.bin.%s:main" % (X,X) for X in binscripts]



#===============================================================================
# Reconfigure build if on readthedocs.org
#
# If on doc server, only require essentials for building package:
#     Cython, numpy, pysam.
#
# Everything else can be mocked
#===============================================================================

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
     install_requires = [
                        SCIPY_VERSION,
                        "pandas>=0.17.0",
                        "matplotlib>=1.4.0",
                        "biopython>=1.64",
                        "twobitreader>=3.0.0",
                        ] + setup_requires
else:
    install_requires = ["cython","numpy","pysam","biopython"]



#===============================================================================
# Custom command classes
#
# If a user supplies CYTHON_ARG on the command line, these invoke
# cythonize on .pyx files to regenerate .c files. If not, existing
# .c files are compiled into .so files or .dlls
#===============================================================================

# options for compilation ------------------------------------------------------

CYTHONIZE_COMMAND = "recythonize" # command-class command from setup.py
CYTHONIZE_ARG = "recythonize"     # '--recythonize', passable to sdist, build_ext et c

CYTHON_ARGS= {
    "embedsignature" : True,
    "language_level" : sys.version_info[0],

    # enable/disable these for development/release
    #"linetrace" : True, # requires passing CYTHON_TRACE=1 to C compiler
    #"profile"   : True,
}


CYTHON_OPTIONS = [
        (CYTHONIZE_ARG,
         None,
         "If supplied, use Cython to regenerate .c sources from pyx files " +\
         "(requires Cython; default False)"
        ),
]

CYTHON_DEFAULTS = [False]
"""Default values for CYTHON_OPTIONS"""



# add headers from numpy & pysam to include paths for pyx, c files
INCLUDE_PATH = []
for mod in (numpy,pysam):
    ipart = mod.get_include()
    if isinstance(ipart,str):
        INCLUDE_PATH.append(ipart)
    elif isinstance(ipart,(list,tuple)):
        INCLUDE_PATH.extend(ipart)
    else:
        raise ValueError("Could not parse include path: %s" % ipart)


# paths to C files and PYX files
base_path = os.getcwd()

PYX_PATHS = glob.glob(os.path.join(base_path,"plastid","genomics","*.pyx"))
"""Paths to Cython .pyx files"""

C_PATHS = [X.replace(".pyx",".c") for X in PYX_PATHS]
"""Potential path to cythonized .c files"""


# default extension modules, C files
ext_modules = [Extension(x.replace(base_path+os.sep,"").replace(".c","").replace(os.sep,"."),
                    [x],include_dirs=INCLUDE_PATH) for x in C_PATHS]


# classes & functions for compilation -----------------------------------------

def wrap_command_classes(baseclass):
    """Add custom command-line `--recythonize` options to distutils/setuptools
    command classes
    
    Parameters
    ----------
    baseclass : setuptools.Command or subclass (not instance!)
        Command class to modify

    Returns
    -------
    class
        Modified class
    """
    class subclass(baseclass):
        user_options = baseclass.user_options + CYTHON_OPTIONS
        new_options = CYTHON_OPTIONS
        new_defaults = CYTHON_DEFAULTS

        def initialize_options(self):
            baseclass.initialize_options(self)
            for (op,_,_), default in zip(self.new_options,
                    self.new_defaults):
                setattr(self,op,default)
        
        def finalize_options(self):
            baseclass.finalize_options(self)
            if "--%s" % CYTHONIZE_ARG in self.distribution.script_args:
                print("Cythonize on")
                setattr(self,CYTHONIZE_ARG,True)

        def run(self):
            have_all = all([os.access(X,os.F_OK) for X in C_PATHS])
            if have_all == False:
                print("Could not find .c files. Regenerating via recythonize.")
                setattr(self,CYTHONIZE_ARG,True)
                self.distribution.script_args.append("--%s" % CYTHONIZE_ARG)
            
            if getattr(self,CYTHONIZE_ARG) == True:
                print("Cythonizing")
                self.run_command(CYTHONIZE_COMMAND)

            return baseclass.run(self)

    subclass.__name__ = "cython_%s" % baseclass.__name__
    return subclass


class clean_c_files(Command):
    """Remove previously generated .c files"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for file_ in C_PATHS:
            if os.access(file_,os.F_OK):
                print("clean_c_files: removing %s..." % file_)
                os.remove(file_)


class build_c_from_pyx(build_ext):
    """Regenerate .c files from pyx files if --CYTHONIZE_ARG or CYTHONIZE_COMMAND is added to command line"""
    user_options = build_ext.user_options + CYTHON_OPTIONS
    new_options  = CYTHON_OPTIONS
    new_defaults = CYTHON_DEFAULTS

    cython_args  = CYTHON_ARGS
    include_path = INCLUDE_PATH
    old_extensions = ext_modules

    def initialize_options(self):
        for (op,_,_), default in zip(self.new_options,
                self.new_defaults):
            setattr(self,op,default)
        build_ext.initialize_options(self)

    def finalize_options(self):
        if "--%s" % CYTHONIZE_ARG in self.distribution.script_args or CYTHONIZE_COMMAND in self.distribution.script_args:
            self.run_command('clean')
            print("build_c_from_pyx: regenerating .c files from Cython")
            from Cython.Build import cythonize
            extensions = cythonize(PYX_PATHS,
                                   include_path=self.include_path,
                                   compiler_directives=self.cython_args)
            self.extensions = extensions

        build_ext.finalize_options(self)

    def run(self): # override so that extensions are only build with build_ext, install, etc
        pass



#===============================================================================
# Program body 
#===============================================================================

FAIL_MSG = """Setup failed. If this is due to a compiler error,
try rebuilding the Cython sources. If installing via pip, make
sure all dependencies are already pre-installed, then separately
run:

    $ pip install --upgrade --install-option="--recythonize" plastid


Or, if installing manually via setup.py:

    $ python setup.py install --recythonize
"""

setup(

    # package metadata
    name             = "plastid",
    version          = plastid_version,
    author           = "Joshua Griffin Dunn",
    author_email     = "joshua.g.dunn@gmail.com",
    maintainer       = "Joshua Griffin Dunn",
    maintainer_email = "Joshua Griffin Dunn",
    long_description =  long_description,

    description      = "Convert genomic datatypes into Pythonic objects useful to the SciPy stack",
    license          = "BSD 3-Clause",
    keywords         = "ribosome profiling riboseq rna-seq sequencing genomics biology",
    url              = "https://github.com/joshuagryphon/plastid",
    download_url     = "https://pypi.python.org/pypi/plastid/",
    platforms        = "OS Independent",
 
    classifiers      = [
         'Development Status :: 4 - Beta',

         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.3',
         'Programming Language :: Python :: 3.4',
         'Programming Language :: Python :: 3.5',

         'Topic :: Scientific/Engineering :: Bio-Informatics',
         'Topic :: Software Development :: Libraries',

         'Intended Audience :: Science/Research',
         'Intended Audience :: Developers',

         'License :: OSI Approved :: BSD License',
         #'Operating System :: OS Independent',
         'Operating System :: POSIX',
         'Natural Language :: English',
    ],


    # packaging info
    packages             = packages,
    package_data         = { "" : ["*.pyx","*.pxd"] }, #,"*.c"], },

    entry_points     = { "console_scripts" : get_scripts()
                       },

    ext_modules = ext_modules,
    cmdclass    = {
                    CYTHONIZE_COMMAND : build_c_from_pyx,
                    'build_ext' : wrap_command_classes(build_ext),
                    #'sdist'     : wrap_command_classes(sdist),
                    'install'   : wrap_command_classes(install),
                    'develop'   : wrap_command_classes(develop),
                    'clean'     : clean_c_files,
                   },

    setup_requires   = setup_requires,
    install_requires = install_requires,
   
    tests_require     = [ "nose>=1.0" ],
    test_suite        = "nose.collector",

)
