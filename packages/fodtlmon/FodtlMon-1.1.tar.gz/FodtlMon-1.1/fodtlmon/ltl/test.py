"""
test file
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
import inspect
import imp
from random import random

ltl = imp.load_source("ltl", "fodtlmon/ltl/ltl.py")


class Fuzzer:
    """
    Monitors tester
    """
    def __init__(self, language, alphabet=None, constants=None):
        self.nodes = []
        self.language = language
        self.constants = [] if constants is None else constants
        self.alphabet = [] if alphabet is None else alphabet

    def init_fuzzer(self):
        ltl = imp.load_source("", "fodtlmon/ltl/ltl.py")
        for name, obj in inspect.getmembers(ltl):
            # TODO : fixe me spacename conflict
            if inspect.isclass(obj):
                # Get only classes that are defined in ltl
                if obj.__module__ == "ltl":
                    # Get only classes inherit from Exp
                    if obj.__base__ is UExp or obj.__base__ is BExp or obj in (true, false, Predicate):
                        if obj is not Release and obj is not R:
                            self.nodes.append(obj)

    def gen(self, depth):
        if depth == 0:
            i = int(random() * 100) % len(self.alphabet)
            j = int(random() * 100) % len(self.constants)
            return P(self.alphabet[i], [Constant(self.constants[j])])

        res = None
        n = int(random()*10)
        node = self.nodes[n % len(self.nodes)]
        if issubclass(node, UExp):
            res = node(self.gen(depth-1))
        elif issubclass(node, BExp):
            res = node(self.gen(depth-1), self.gen(depth-1))
        elif node in (true, false):
            res = node()
        elif node is Predicate:
            i = int(random() * 100) % len(self.alphabet)
            j = int(random() * 100) % len(self.constants)
            res = P(self.alphabet[i], [Constant(self.constants[j])])
        return res

    def gen_trace(self, length, max_depth=2, depth=0, preds=None):
        trace = Trace()
        for x in range(length):
            i = int(random() * 10) % len(self.alphabet)
            j = int(random() * 10) % len(self.constants)
            dp = int(random() * 10) % max_depth if depth == 0 else depth
            e = Event()
            for y in range(dp):
                res = P(self.alphabet[i], [Constant(self.constants[j])])
                if preds is not None:
                    if res.isIn(preds):
                        e.push_predicate(res)
                else:
                    e.push_predicate(res)
            trace.push_event(e)
        return trace


###########################
# Main tester
###########################
def print2(*args, file=None):
    # print(*args)
    if file is not None:
        file.write(*args)
        file.write("\n")


def run_ltl_tests(monitor="ltl", formula_nbr=1, formula_depth=2, trace_lenght=5, trace_depth=1,
              alphabet=None, constants=None, interactive=False, output_file="fodtlmon/tests/logs.log", debug=False):

    fuzzer = Fuzzer(monitor, alphabet=alphabet, constants=constants)
    fuzzer.init_fuzzer()
    errors = 0
    nbr = formula_nbr
    nbr = 1
    formula_depth = 1
    formula_nbr = 1
    with open(output_file, "w+") as f:
        for x in range(nbr):
            print("## %s / %s  Errors %s" % (x+1, nbr, errors))
            formula = fuzzer.gen(formula_depth)
            trace = fuzzer.gen_trace(trace_lenght, depth=trace_depth, preds=formula.walk(filter_type=P))
            print2("\n\n============ LTLMON : ", file=f)
            print2("Formula   : %s\nFormula C : %s\nTrace     : %s" % (formula, formula.toCODE(), trace), file=f)
            res1 = Ltlmon(formula, trace).monitor(debug=debug)
            print2(res1, file=f)

            print2("\n============ LTLFO2MON : ", file=f)
            fl = formula.toLTLFO()
            tr = trace.toLTLFO()
            print2("Formula : %s\nTrace   : %s" % (fl, tr), file=f)
            res2 = str(ltlfo2mon(fl, tr))
            print2(res2, file=f)

            # res11 = res1.replace("Result Progression: ", "")[0]
            # res22 = res2.replace("Result Progression: ", "")[0]
            if res1 != res2:
                errors += 1
                print2("\n## Result are different ! ", file=f)
                print2(res1, file=f)
                print2(res2, file=f)
                if interactive:
                    debug2 = input("Debug y/n : ")
                    if debug2 == "y":
                         Ltlmon(formula, trace).monitor(debug=debug)
                         input()

        print2("\n\n#####\nResult : %s / %s" % (nbr-errors, nbr), file=f)
