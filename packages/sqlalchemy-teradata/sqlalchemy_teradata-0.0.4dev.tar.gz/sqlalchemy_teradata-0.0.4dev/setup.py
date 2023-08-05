# The MIT License (MIT)
#
# Copyright (c) 2015 by Teradata
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='sqlalchemy_teradata',
    version='0.0.4',
    description="Teradata dialect for SQLAlchemy",
    classifiers=[
                      'Development Status :: 3 - Alpha',
                      'Environment :: Console',
                      'Intended Audience :: Developers',
                      'Programming Language :: Python',
                      'Programming Language :: Python :: 3',
                      'Programming Language :: Python :: Implementation :: CPython',
                      'Topic :: Database :: Front-Ends',
                ],
    keywords='Teradata SQLAlchemy',
    author='Mark Sandan',
    author_email='mark.sandan@teradata.com',
    license='MIT',
    packages=['sqlalchemy_teradata', 'test'],
    include_package_data=True,
    tests_require=['pytest >= 2.5.2'],
    install_requires=['teradata'],
    entry_points={
                'sqlalchemy.dialects': [
                           'teradata = sqlalchemy_teradata.dialect:TeradataDialect',
                                           ]
                }
)
