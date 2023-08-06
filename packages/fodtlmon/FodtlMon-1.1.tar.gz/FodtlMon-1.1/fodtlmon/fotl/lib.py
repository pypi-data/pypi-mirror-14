"""
lib LTL monitor
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
__author__ = 'walid'

from fodtlmon.fotl.fotl import *
import re


class Eq(BIO):
    """ Equality operator """
    operator = "=="
    cast = str


class Gt(BIO):
    """ Greater than """
    operator = ">"
    cast = int


class Lt(BIO):
    """ Less than """
    operator = "<"
    cast = int


class NEq(BIO):
    """ Not equal """
    operator = "!="
    cast = str


class Regex(IP):
    """ Regular expression """
    def eval(self, valuation=None, trace=None):
        args2 = super().eval(valuation=valuation, trace=trace)
        p = re.compile(str(args2[1].name))
        return False if p.match(args2[0].name) is None else True


class In(BIO):
    """ In """
    operator = "in"
    cast = str


class InTrace(IP):
    """ Check if a predicate is in the trace """
    def eval(self, valuation=None, trace=None):
        args2 = super().eval(valuation=valuation, trace=trace)
        return trace.contains(Predicate.parse(str(args2[0].name)))


####################
# Math functions
####################
class MathFx(BFX):
    """ Default math function : Do not use directly """
    cast = float
    return_cast = float


class Add(MathFx):
    """ Addition """
    operator = "+"


class Sub(BFX):
    """ Subtraction """
    operator = "-"


class Mul(BFX):
    """ Multiplication """
    operator = "*"


class Div(BFX):
    """ Division """
    operator = "/"
