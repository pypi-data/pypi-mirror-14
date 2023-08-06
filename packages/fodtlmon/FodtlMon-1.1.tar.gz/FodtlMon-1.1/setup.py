"""
fodtlmon version 1.0
Copyright (C) 2015 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from distutils.core import setup

setup(
    name='fodtlmon',
    version='1.1',
    packages=['fodtlmon', 'fodtlmon.parser', 'fodtlmon.dtl', 'fodtlmon.fodtl', 'fodtlmon.fotl', 'fodtlmon.ltl', 'fodtlmon.tools', 'fodtlmon.webservice'],
    url='https://github.com/hkff/fodtlmon',
    license='GPL3',
    author='Walid Benghabrit',
    author_email='benghabrit.walid@gmail.com',
    description='FODTLMON is a monitoring framework based on distributed first order linear temporal logic.',
    install_requires=[
        'antlr4-python3-runtime>=4.5',
    ]
)
