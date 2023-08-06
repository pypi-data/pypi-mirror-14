"""
fotlmon FOTL monitor
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
from fodtlmon.ltl.ltlmon import *
from fodtlmon.fotl.fotl import *
from fodtlmon.fotl.lib import *
# step = 0


class Fotlmon(Ltlmon):
    """
    Fotl monitoring using progression technique
    """
    def prg(self, formula, event, valuation=None):
        # global step

        if valuation is None:
                valuation = []

        if isinstance(formula, Predicate):
            # Overrides the Predicate test of Ltlmon
            # Check in trace if event contains P with for all linked vars
            res = true() if event.contains(formula.instantiate(valuation)) else false()

        elif isinstance(formula, Forall):
            elems = []
            for p in event.predicates:
                if p.name == formula.var.vtype:
                    valuation2 = []
                    valuation2.extend(valuation)
                    for v in p.args:
                        # Bind the value of the variable in the predicate
                        # with the variable name in the VarDec
                        valuation2.append(Valuation(v, formula.var.name))
                    # Add the formula with the valuation for the variable
                    elems.append(ForallConjNode(formula.inner, valuation2))
            res = self.prg(ForallConj(elems), event, valuation)

        elif isinstance(formula, ForallConj):
            e = []
            for x in formula.inner:
                # Eval all nodes with their eval2
                e.append(ForallConjNode(self.prg(x.formula, event, x.valuation), valuation))
            res = ForallConj(e).eval()
            # return res

        elif isinstance(formula, IPredicate):
            res = B3(formula.eval(valuation=valuation, trace=self.trace))

        elif isinstance(formula, Function):
            res = formula.eval(valuation=valuation, trace=self.trace)

        else:
            res = super().prg(formula, event, valuation)

        # print("-- step %s -- %s ...... res %s " % (step, formula, res))
        # step += 1
        return res


class ForallConj(UExp):
    """
    Forall Conjunction (internal for monitor)
    """
    symbol = "\u2227"

    def __init__(self, inner=None):
        super().__init__(inner)

    def eval(self):
        elems2 = list(filter(lambda x: not (isinstance(x.formula, true) or x.formula is Boolean3.Top), self.inner))
        if len(elems2) == 0:
            return Boolean3.Top
        elif len(list(filter(lambda x: isinstance(x.formula, false) or x.formula is Boolean3.Bottom, self.inner))) > 0:
            return Boolean3.Bottom
        else:
            return ForallConj(elems2)

    def __str__(self):
        return "%s (%s)" % (self.symbol, ", ".join([str(x) for x in self.inner]))


class ForallConjNode:
    """
    Forall conjunction node contains formula -> evaluation
    """
    def __init__(self, formula=None, valuation=None):
        self.formula = formula
        self.valuation = valuation

    def __str__(self):
        return "(%s : %s)" % (self.formula, ",".join([str(x) for x in self.valuation]))
