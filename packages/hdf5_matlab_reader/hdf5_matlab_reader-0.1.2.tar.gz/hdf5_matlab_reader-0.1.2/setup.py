import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name="hdf5_matlab_reader",
    version="0.1.2",
    maintainer="Roan LaPlante",
    maintainer_email="rlaplant@nmr.mgh.harvard.edu",
    description=("HDF5 Matlab Reader"),
    license="Visuddhimagga Sutta; GPLv3+",
    long_description=read('readme.md'),
    datafiles=[('', ['readme.md', 'LICENSE'])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    url="https://github.com/aestrivex/hdf5_matlab_reader",
    platforms=['any'],
    packages=['hdf5_matlab_reader'],
    install_requires=["numpy", "scipy", "h5py"]
)
