# coding=utf-8
from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='bubblepy',
    version='1.0',
    py_modules=['bubblepy'],
    author='Szymon Pyżalski',
    author_email='zefciu <szymon@pythonista.net>',
    url='https://github.com/zefciu/bubblepy',
    description='Bubble Babble Binary Data Encoding',
    long_description=long_description,
    install_requires=['six>=1.10.0'],
    tests_require = ['nose>=1.0', 'nose-cov>=1.0'],
    test_suite = 'nose.collector',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
