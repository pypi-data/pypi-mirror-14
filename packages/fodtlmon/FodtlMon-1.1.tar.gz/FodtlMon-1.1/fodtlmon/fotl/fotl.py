"""
fotl
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
from fodtlmon.ltl.ltl import *


#############################
# FO Operators
#############################
class Forall(UExp):
    """
    Forall operator
    """
    symbol = "\u2200"

    def __init__(self, var=None, inner=None):
        super().__init__(inner)
        self.var = var

    def toTSPASS(self):
        return "![%s](%s)" % (self.var.toTSPASS(), self.inner.toTSPASS())

    def toLTLFO(self):
        return "A %s. (%s)" % (self.var.toLTLFO(), self.inner.toLTLFO())

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.var.toCODE(), self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, str(self.var), self.inner)


class Exists(Neg):
    """
    Exsits operator
    """
    symbol = "\u2203"

    def __init__(self, var=None, inner=None):
        self.var = var
        self.inner2 = inner
        super().__init__(inner=Forall(var=var, inner=Neg(inner)))

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, str(self.var), self.inner2)

    def prefix_print(self):
        return "(%s %s %s)" % (self.symbol, self.var, self.inner2.prefix_print())

    def toCODE(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.var.toCODE(), self.inner2.toCODE())

    def toTSPASS(self):
        return "?[%s](%s)" % (self.var.toTSPASS(), self.inner2.toTSPASS())

    def toLTLFO(self):
        return "E %s. (%s)" % (self.var.toLTLFO(), self.inner2.toLTLFO())


class VarDec(Exp):
    """
    Variable declaration
    """
    def __init__(self, name="", vtype=""):
        self.name = name
        self.vtype = vtype

    def toTSPASS(self):
        return "%s:%s" % (self.name, self.vtype)

    def toLTLFO(self):
        return "%s:%s" % (self.name, self.vtype)

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s('%s', '%s')" % (self.__class__.__name__, self.name, self.vtype)

    def eval(self):
        return self

    def __str__(self):
        return "%s:%s" % (self.name, self.vtype)

VD = VarDec


class Valuation:
    """
    Valuation links between value and var name
    """
    def __init__(self, value=None, var=None):
        self.value = value
        self.var = var

    def __str__(self):
        return "%s<-%s" % (self.value, self.var)


#############################
# Functions / Interpreted OP
#############################
class MetaBase(type):
    """
    Metaclass to register all IPredicates and functions
    """
    classes = []

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(cls, name, bases)
        MetaBase.classes.append(cls)


class IPredicate(Exp, metaclass=MetaBase):
    """
    Interpreted Predicate
    """
    def __init__(self, *args):
        # IMPORTANT : Test the size of args, because of subclass super call
        self.args = list(args[0] if len(args) == 1 else args)

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, ",".join([str(x) for x in self.args]))

    def toCODE(self):
        return "%s(%s)" % (self.__class__.__name__, ",".join([str(x) for x in self.args]))

    @staticmethod
    def get_class_from_name(klass):
        return next(filter(lambda x: not issubclass(x, Function) and x.__name__ == klass, MetaBase.classes), None)

    def eval(self, valuation=None, trace=None):
        """
        This method should be always called by subclasses
        :param valuation
        :param trace
        :return: Arguments evaluation
        """
        args2 = []
        for a in self.args:
            if isinstance(a, Function) or isinstance(a, IPredicate):
                args2.append(Constant(a.eval(valuation=valuation, trace=trace)))

            elif isinstance(a, Variable):
                found = False
                for v in valuation:
                    if str(v.var) == a.name:
                        args2.append(Constant(str(v.value.name)))
                        found = True
                        break
                if not found:
                    raise Exception("IPredicate instantiation failed : missing vars")
            else:
                args2.append(Constant(a))

        return args2

IP = IPredicate


class BIOperator(IPredicate):
    """
    Binary Interpreted operator
    """
    operator = None
    cast = str

    def eval(self, valuation=None, trace=None):
        args2 = super().eval(valuation=valuation, trace=trace)
        return eval("\"%s\" %s \"%s\"" % (self.cast(args2[0].name), self.operator, self.cast(args2[1].name)))

BIO = BIOperator


class Function(IPredicate):
    """
    Function
    """
    def eval(self, valuation=None, trace=None):
        """
        This method should be override to return some value
        :param valuation
        :param trace
        :return:
        """
        return super().eval(valuation=valuation, trace=trace)

    @staticmethod
    def get_class_from_name(klass):
        return next(filter(lambda x: issubclass(x, Function) and x.__name__ == klass, MetaBase.classes), None)

FX = Function


class BFunction(Function):
    """
    Binary Function
    """
    operator = None
    cast = str
    return_cast = str

    def eval(self, valuation=None, trace=None):
        args2 = super().eval(valuation=valuation, trace=trace)
        return self.return_cast(eval("%s %s %s" % (self.cast(args2[0].name), self.operator, self.cast(args2[1].name))))

BFX = BFunction
