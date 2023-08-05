"""Airport List Query setup package.

See:
https://github.com/MatthieuMichon/aplist
"""

from setuptools import setup

setup(
    name='aplist',
    version='0.1.dev6',
    description='Airport List Query module',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
    ],
    url='https://github.com/MatthieuMichon/aplist',
    author='Matthieu Michon',
    author_email='matthieu.michon@gmail.com',
    license='GPLv3',
    packages=['aplist'],
    install_requires=[
          'requests',
    ],
    test_suite='tests',
    zip_safe=False
)
