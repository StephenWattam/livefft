from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='livefftsdl',
    version='0.1.0',
    description='A live FFT visualisation using SDL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/StephenWattam/livefftsdl'
    author='Steve Wattam; Rick Lupton',
    author_email='steve@stephenwattam.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='audio visualisation fft',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    install_requires=['numpy==1.17.2', 'PyAudio==0.2.11', 'PyQt5==5.13.0', 'PyQt5-sip==4.19.18',
                       'pyqtgraph==0.10.0', 'PySDL2==0.9.6'],
    extras_require={
        'dev': [],
        'test': [], # TODO!
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'fonts': ['fonts/tuffy.ttf'],
    },
    # data_files=[('my_data', ['data/data_file'])],
    entry_points={  # Optional
        'console_scripts': [
            'livefftsdl=livefftsdl:run',
        ],
    },

    project_urls={  # Optional
        'Say Thanks!': 'https://stephenwattam.com/contact/',
        'Source': 'https://github.com/StephenWattam/livefftsdl',
    },
)

