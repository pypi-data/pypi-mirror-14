import os.path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(
    name='envfile',
    version='1.0',
    description='Run a command using a modified environment configured in an INI file',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
    ],
    py_modules=['envfile'],
    author='Laurence Rowe',
    author_email='laurence@lrowe.co.uk',
    url='http://github.com/lrowe/envfile',
    license='MIT',
    entry_points={
        'console_scripts': ['envfile = envfile:main'],
    },
)
