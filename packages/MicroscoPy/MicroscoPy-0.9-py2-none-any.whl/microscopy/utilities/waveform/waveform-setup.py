from distutils.core import setup

setup(
    name = 'waveform',
    version = '1.0',
    description = 'A simple package to manipulate and plot time waveforms',
    author = 'Guillaume Lepert',
    author_email = 'guillaume.lepert07@imperial.ac.uk',
    long_description="""
    A Waveform class to create, manipulate and plot functions of time.
    
    It was primarily designed to work with the analog input/output functions
    of the MCCDAQ Python driver, but is much more general in scope.

    The main functionalities include:
    
    - multi-channel waveforms
    
    - define complex waveforms (for analog output scans)
    
    - time plots
    
    - XY plots
    
    - XYZ plots (both regularly and randomly spaced data
    
    - Fourier transform.
    """,
    url="https://testpypi.python.org/pypi/mccdaq",
    py_modules = ['waveform'],
    requires=['matplotlib', 'numpy'],
    platforms=['all']
)