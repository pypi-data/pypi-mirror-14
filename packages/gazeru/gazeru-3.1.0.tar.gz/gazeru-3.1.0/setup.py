from setuptools import setup, find_packages
from os import path
import subprocess

here = path.abspath(path.dirname(__file__))
subprocess.call('pandoc {0}/README.md -s -o {0}/README.rst'
                .format(here), shell=True)
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gazeru',
    version='3.1.0',
    description='A crawler for niconico',
    long_description=long_description,
    url='http://github.com/roronya/gazeru',
    author='roronya',
    author_email='roronya628@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='niconico crawler',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests', 'beautifulsoup4', 'nicopy', 'mutagen'],
    scripts=['bin/gazeru']
)
