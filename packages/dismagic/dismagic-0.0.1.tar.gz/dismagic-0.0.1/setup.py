from setuptools import setup

README = open('README.rst').read()

setup(
    name='dismagic',
    version='0.0.1',
    description="An extension for IPython that help to disassembly source and objects.",
    long_description=README,
    author='Marshalov Alexander',
    author_email='_@marshalov.org',
    url='https://github.com/amper/dismagic',
    license='BSD',
    keywords="ipython notebook dis disassembly disassembling",
    py_modules=['dismagic'],
    install_requires=['ipython'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Plugins',
        'Environment :: Plugins',
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Disassemblers',
    ],
)
