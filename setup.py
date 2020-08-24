# OLIB - the object library !
#
#

from setuptools import setup

setup(
    name='oklib',
    version='4',
    url='https://github.com/bthate/oklib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OKLIB is a library with basic console/clock/parse/handle functionality. no copyright or LICENSE. placed in the Public Domain.",
    long_description="OKLIB has all you need to write a standard application.",
    license='Public Domain',
    install_requires=["olib>=2"],
    zip_safe=False,
    packages=["ok"],
    namespace_packages=["ok"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
