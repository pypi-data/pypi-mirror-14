import os.path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(
    name='pytest_exact_fixtures',
    version='0.1',
    description='Parse queries in Lucene and Elasticsearch syntaxes',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Intended Audience :: Developers",
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
    packages=['pytest_exact_fixtures'],
    author='Laurence Rowe',
    author_email='laurence@lrowe.co.uk',
    url='http://github.com/lrowe/pytest_exact_fixtures',
    license='MIT',
    requires=['pytest'],
    entry_points={
        'pytest11': ['pytest_exact_fixtures = pytest_exact_fixtures'],
    },
)
