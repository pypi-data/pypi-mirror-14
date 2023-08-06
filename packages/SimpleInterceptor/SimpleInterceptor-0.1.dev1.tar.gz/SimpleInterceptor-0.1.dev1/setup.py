"""Setup module"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SimpleInterceptor',
    version='0.1.dev1',
    description='Simple interceptor related to concepts of AOP',
    long_description=long_description,
    url='https://github.com/host-anshu/simpleInterceptor',
    author='Anshu Choubey',
    author_email='anshu.choubey@imaginea.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='interceptor aop',
    packages=find_packages(),
    py_modules=['interceptor'],
    entry_points={
        'console_scripts': [
            'interceptor=interceptor:intercept',
        ],
    },
    test_suite="test"
)