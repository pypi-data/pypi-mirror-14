import setuptools
import setuptools.command.test

import pynetics

setuptools.setup(
    name='pynetics',
    version=pynetics.__version__,
    url='http://github.com/blazaid/pynetics/',
    license='GNU General Public License v3',
    author='blazaid',
    tests_require=[],
    install_requires=[],
    author_email='alberto.da@gmail.com',
    description='An evolutionary computation library for Python',
    long_description=open('README.rst').read(),
    packages=['pynetics', 'pynetics.gggp', ],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
