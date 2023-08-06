"""
ltl
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
import re

__author__ = 'walid'
from enum import Enum


#############################
# Abstract operators
#############################

class Formula:
    """
    Abstract formula
    """
    symbol = ""
    tspass = ""
    ltlfo = ""
    code = ""

    def toTSPASS(self):
        return str(self)

    def toLTLFO(self):
        return str(self)

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return self.__class__.__name__ + "()"

    def reduce(self):
        pass

    def eval(self):
        return self

    def clos(self):
        pass

    def nnf(self):
        pass

    def and_(self, exp):
        return And(self, exp)

    def or_(self, exp):
        return Or(self, exp)

    def size(self):
        return 1 + sum([s.size() for s in self.children()])

    def children(self):
        return []

    def walk(self, filters: str=None, filter_type: type=None, pprint=False, depth=-1):
        """
        Iterate tree in pre-order wide-first search order

        :param filters: filter by python expression
        :param filter_type: Filter by class
        :return:
        """
        children = self.children()
        if children is None:
            children = []
        res = []

        if depth == 0:
            return res
        elif depth != -1:
            depth -= 1

        for child in children:
            if isinstance(child, Formula):
                tmp = child.walk(filters=filters, filter_type=filter_type, pprint=pprint, depth=depth)
                if tmp:
                    res.extend(tmp)

        if filter_type is None:
            if filters is not None:
                if eval(filters) is True:
                    res.append(self)
            else:
                res.append(self)
        elif isinstance(self, filter_type):
            if filters is not None:
                if eval(filters) is True:
                    res.append(self)
            else:
                res.append(self)

        if pprint:
            res = [str(x) + " " for x in res]
            res = "\n".join(res)
        return res


class Exp(Formula):
    pass


class Atom(Exp):
    """
    Atom
    """
    symbol = ""

    def __str__(self):
        return str(self.symbol)


class true(Atom):
    """
    True
    """
    symbol = "true"

    def eval(self):
        return true()

    # def and_(self, exp):
    #     if isinstance(exp, true): return true()
    #     elif isinstance(exp, false): return false()
    #     else: return exp
    #
    # def or_(self, exp):
    #     return self


class false(Atom):
    """
    False
    """
    symbol = "false"

    def eval(self):
        return false()

    # def and_(self, exp):
    #     return self
    #
    # def or_(self, exp):
    #     if isinstance(exp, true): return true()
    #     elif isinstance(exp, false): return false()
    #     else: return exp


class Parameter(Exp):
    """
    Parameter
    """
    def __init__(self, name=""):
        self.name = str(name)

    def __str__(self):
        return "%s" % self.name

    def equal(self, o):
        return (o is not None) and isinstance(o, Parameter) and (o.name == self.name)

    def toCODE(self):
        return "%s('%s')" % (self.__class__.__name__, self.name)

    @staticmethod
    def parse(string: str, cts=False):
        string = string.strip()
        if (string.startswith("'") and string.endswith("'")) or (string.startswith('"') and string.endswith('"')):
            return Constant(string[1:-1])
        elif cts:
            return Constant(string)
        else:
            return Variable(string)


class Variable(Parameter):
    """
    Data variable
    """
    def equal(self, o):
        return (o is not None) and (isinstance(o, Variable) and (o.name == self.name))

    def toLTLFO(self):
        return "%s" % self.name

V = Variable


class Constant(Parameter):
    """
    Constant
    """
    def __init__(self, name=""):
        super().__init__(name=name)
        if self.name.startswith("'") and self.name.endswith("'"):
            self.name = self.name[1:-1]

    def equal(self, o):
        if isinstance(o, Regexp):
            return o.equal(self)
        return (o is not None) and (isinstance(o, Constant) and (str(o.name) == str(self.name)))

    def toLTLFO(self):
        return "'%s'" % self.name

    def __str__(self):
        return "'%s'" % self.name

C = Constant


class Regexp(Constant):
    """
    regexp
    """
    def equal(self, o):
        try:
            if o is not None:
                p = re.compile(str(self.name))
                return False if p.match(o.name) is None else True
        except:
            return False


class Predicate(Exp):
    """
    Predicate
    """
    def __init__(self, name="", args=None):
        if args is None:
            p = Predicate.parse(name)
            self.name = p.name
            self.args = p.args
        else:
            self.name = name
            self.args = args

    def __str__(self):
        args = ",".join([str(p) for p in self.args])
        return "%s(%s)" % (self.name, args)

    @staticmethod
    def parse(string: str, cts=False):
        string = string.strip()
        if string.endswith(")"):
            name = string[0: string.find("(")]
            args = string[string.find("(")+1:-1].split(",")
            arguments = []
            for ar in args:
                if ar != '':
                    arguments.append(Parameter.parse(ar, cts=cts))
        else:
            print("Invalid predicate format !")
            return
        return Predicate(name, arguments)

    def equal(self, p):
        res = False
        if isinstance(p, Predicate):
            res = (p.name == self.name) and (len(p.args) == len(self.args))
            if res:
                for a1, a2 in zip(self.args, p.args):
                    if not a1.equal(a2):
                        return False
        return res

    def toLTLFO(self):
        args = ",".join([p.toLTLFO() for p in self.args])
        return "%s(%s)" % (self.name, args)

    def toCODE(self):
        args = ",".join([p.toCODE() for p in self.args])
        return "%s('%s', %s)" % (self.__class__.__name__, self.name, "[" + args + "]")

    def children(self):
        return self.args

    def isIn(self, preds):
        for x in preds:
            if self.equal(x):
                return True
        return False

    def instantiate(self, valuation):
        p = Predicate(name=self.name, args=[])
        for x in self.args:
            if isinstance(x, Variable):
                # Lookup in valuation
                found = False
                for v in valuation:
                    if str(v.var) == x.name:
                        p.args.append(Constant(str(v.value.name)))
                        found = True
                        break
                if not found:
                    # raise Exception("Predicate instantiation failed : missing vars")
                    # p.args.append(Variable(str(x.name)))
                    return None

            elif isinstance(x, Constant):
                p.args.append(x)
        return p

P = Predicate


class UExp(Exp):
    """
    Unary expression
    """
    symbol = ""

    def __init__(self, inner=None):
        self.inner = inner

    def __str__(self):
        return "%s(%s)" % (self.symbol, self.inner)

    def prefix_print(self):
        return "(%s %s)" % (self.symbol, self.inner.prefix_print())

    def toTSPASS(self):
        return "(%s %s)" % (self.tspass, self.inner.toTSPASS())

    def toLTLFO(self):
        return "(%s %s)" % (self.ltlfo, self.inner.toLTLFO())

    def toCODE(self):
        return "%s(%s)" % (self.__class__.__name__, self.inner.toCODE())

    def children(self):
        return [self.inner]


class BExp(Exp):
    """
    Binary expression
    """
    symbol = ""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.left, self.symbol, self.right)

    def prefix_print(self):
        return "(%s %s %s)" % (self.symbol, self.left, self.right)

    def toTSPASS(self):
        return "(%s %s %s)" % (self.left.toTSPASS(), self.tspass, self.right.toTSPASS())

    def toLTLFO(self):
        return "(%s %s %s)" % (self.left.toLTLFO(), self.ltlfo, self.right.toLTLFO())

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.left.toCODE(), self.right.toCODE())

    def children(self):
        return [self.left, self.right]


#############################
# LTL Operators
#############################

##
# Propositional operators
##
class And(BExp):
    symbol = "and"
    tspass = "&&"
    ltlfo = "/\\"

    def eval(self):
        # return self.left.eval().and_(self.right.eval())
        if isinstance(self.left, true) or self.left is Boolean3.Top:
            return self.right
        elif isinstance(self.left, false) or self.left is Boolean3.Bottom:
            return false()
        else:
            if isinstance(self.right, true) or self.right is Boolean3.Top: return self.left
            elif isinstance(self.right, false) or self.right is Boolean3.Bottom: return false()
            else: return self

    # def and_(self, exp):
    #     return self.left.and_(self.right)
    #
    # def or_(self, exp):
    #     return self.left.or_(self.right)


class Or(BExp):
    symbol = "or"
    tspass = "||"
    ltlfo = "\/"

    def eval(self):
        # return self.left.eval().or_(self.right.eval())
        if isinstance(self.left, true) or self.left is Boolean3.Top:
            return true()
        elif isinstance(self.left, false) or self.left is Boolean3.Bottom:
            return self.right
        else:
            if isinstance(self.right, true) or self.right is Boolean3.Top: return true()
            elif isinstance(self.right, false) or self.right is Boolean3.Bottom: return self.left
            else: return self

    # def and_(self, exp):
    #     return self.left.and_(self.right)
    #
    # def or_(self, exp):
    #     return self.left.or_(self.right)


class Neg(UExp):
    symbol = "not"
    tspass = "~"
    ltlfo = "~"

    def eval(self):
        if isinstance(self.inner, true) or self.inner is Boolean3.Top: return false()
        elif isinstance(self.inner, false) or self.inner is Boolean3.Bottom: return true()
        elif isinstance(self.inner, Neg): return self.inner.inner
        else: return self

Not = Neg


class Imply(Or):
    symbol = "=>"
    tspass = "=>"
    ltlfo = "=>"

    def __init__(self, left=None, right=None):
        super().__init__(Neg(left), right)

    def __str__(self):
        return "(%s %s %s)" % (self.left.inner, self.symbol, self.right)

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.left.inner.toCODE(), self.right.toCODE())


##
# Temporal operators
##

# Always
class Always(UExp):
    symbol = "always"
    tspass = "always"
    ltlfo = "G"


class G(Always):
    symbol = "G"


# Future
class Future(UExp):
    symbol = "future"
    tspass = "sometime"
    ltlfo = "F"


class F(Future):
    symbol = "F"


# Next
class Next(UExp):
    symbol = "next"
    tspass = "next"
    ltlfo = "X"


class X(Next):
    symbol = "X"


# Until
class Until(BExp):
    symbol = "until"
    tspass = "until"
    ltlfo = "U"


class U(Until):
    symbol = "U"


# Release
class Release(BExp):
    symbol = "release"
    tspass = "unless"
    ltlfo = ""

    def toLTLFO(self):
        """ Change to until form """
        return "~(~(%s) U ~(%s))" % (self.left.toLTLFO(), self.right.toLTLFO())


class R(Release):
    symbol = "R"


#############################
# Trace / Events
#############################
class Event:
    """
    Event that contains a set of predicates
    """
    def __init__(self, predicates=None, step="0"):
        self.predicates = [] if predicates is None else predicates
        self.step = step

    def __str__(self):
        return "{" + " | ".join([str(p) for p in self.predicates]) + "}"

    @staticmethod
    def parse(string):
        string = string.strip()
        predicates = []
        if string.startswith("{") and string.endswith("}"):
            prs = string[1:-1].split("|")
            if len(prs) == 1 and prs[0] is "":
                return Event()
            for p in prs:
                predicates.append(Predicate.parse(p, cts=True))
        else:
            print("Invalid event format ! A trace should be between {}")
            return
        return Event(predicates)

    def push_predicate(self, predicate):
        self.predicates.append(predicate)
        return self

    def contains(self, predicate):
        for p in self.predicates:
            if isinstance(p, Predicate):
                if p.equal(predicate):
                    return True
        return False

    p = push_predicate

    def toLTLFO(self):
        return "{" + ",".join([p.toLTLFO() for p in self.predicates]) + "}"


class Trace:
    """
    Trace that contains a set of event
    """
    def __init__(self, events=None):
        self.events = [] if events is None else events

    def __str__(self):
        return ";".join([str(e) for e in self.events])

    @staticmethod
    def parse(string):
        string = string.strip()
        events = []
        evs = string.split(";")
        [events.append(Event.parse(e)) if e != "" else None for e in evs]
        return Trace(events)

    def push_event(self, event):
        self.events.append(event)
        return self

    def contains(self, f):
        if isinstance(f, Event):
            return f in self.events
        elif isinstance(f, Predicate):
            for e in self.events:
                if e.contains(f): return True
            return False
        else:
            return False

    e = push_event

    def toLTLFO(self):
        return ",".join([e.toLTLFO() for e in self.events])


#############################
# Three valued boolean
#############################

class Boolean3(Enum):
    """
    Boolean3 values
    """
    Top = "\u22A4"
    Bottom = "\u22A5"
    Unknown = "?"

    def __str__(self):
        return self.value


def B3(formula):
    """
    Rewrite formula eval result into Boolean3
    :param formula:
    :return: Boolean3
    """
    if isinstance(formula, true) or formula is True or formula == Boolean3.Top.name:
        return Boolean3.Top
    if isinstance(formula, false) or formula is False or formula == Boolean3.Bottom.name:
        return Boolean3.Bottom
    else:
        return Boolean3.Unknown

