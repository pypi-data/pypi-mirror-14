from setuptools import setup

import sys

setup(  name='lerpn',
        version='5',
        description='Linux? Engineering RPN calculator',
        url='https://github.com/cpavlina/lerpn',
        download_url = 'https://github.com/cpavlina/lerpn/tarball/5',
        author='Chris Pavlina',
        author_email='pavlina.chris@gmail.com',
        packages=['LerpnApp'],
        entry_points = {
            'console_scripts': [
                'lerpn = LerpnApp:main',
                ],
        },
        keywords = ['calculator', 'rpn'],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console :: Curses",
            "Topic :: Utilities",
            "License :: Public Domain" ]
        )
