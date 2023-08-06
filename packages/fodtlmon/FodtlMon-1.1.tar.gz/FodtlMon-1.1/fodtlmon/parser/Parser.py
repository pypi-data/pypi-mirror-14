"""
fodtl parser
Copyright (C) 2016 Walid Benghabrit

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

from fodtlmon.fodtl.fodtl import *
from fodtlmon.parser.FODTLListener import *
from fodtlmon.parser.FODTLLexer import *
from antlr4.InputStream import *
from antlr4.tree.Trees import Trees


class FodtlParser(ParseTreeListener):

    def __init__(self):
        self.formula = None
        self.formulas = []

    def exitMain(self, ctx:FODTLParser.MainContext):
        pass

    #############################
    # Classical logic
    #############################
    def exitTrue(self, ctx:FODTLParser.TrueContext):
        self.formulas.append(true())

    def exitFalse(self, ctx:FODTLParser.FalseContext):
        self.formulas.append(false())

    def exitConstant(self, ctx:FODTLParser.ConstantContext):
        name = ""
        if ctx.ID() is not None:
            name = str(ctx.ID())
        elif ctx.INT() is not None:
            name = str(ctx.INT())
        self.formulas.append(Constant(name))

    def exitRegexp(self, ctx:FODTLParser.RegexpContext):
        name = ""
        if ctx.STRING() is not None:
            name = str(ctx.STRING())
        self.formulas.append(Regexp(name[1:-1]))

    def exitVariable(self, ctx:FODTLParser.VariableContext):
        name = str(ctx.ID()) if ctx.ID() is not None else ""
        self.formulas.append(Variable(name))

    def exitPredicate(self, ctx:FODTLParser.PredicateContext):
        # TODO handle interpreted predicates and functions
         if len(self.formulas) >= len(ctx.arg()):
            name = str(ctx.ID()) if ctx.ID() is not None else ctx.ID()
            args = []
            for x in range(len(ctx.arg())):
                args.append(self.formulas.pop())
            args.reverse()

            obj = Predicate
            # Check if it's an interpreted predicate
            klass = IPredicate.get_class_from_name(name)
            if klass is not None:
                obj = klass(tuple(args))
            else:
                # Check if it's a function
                klass = Function.get_class_from_name(name)
                if klass is not None:
                    obj = klass(tuple(args))
                else:
                    # It's an uninterpreted predicate
                    obj = Predicate(name, args)

            # Add to the stack
            self.formulas.append(obj)

    def exitFormula(self, ctx:FODTLParser.FormulaContext):
        # Testing boolean operators
        if (ctx.O_and() or ctx.O_or() or ctx.O_imply()) is not None:
            if len(self.formulas) > 1:
                f2 = self.formulas.pop()
                f1 = self.formulas.pop()
                if ctx.O_and() is not None: klass = And
                elif ctx.O_or() is not None: klass = Or
                elif ctx.O_imply() is not None: klass = Imply
                else: raise Exception("Type error")
                self.formulas.append(klass(f1, f2))
            else:
                raise Exception("Missing arguments")
        # Testing Unary temporal operators
        elif ctx.utOperators() is not None:
            if len(self.formulas) > 0:
                inner = self.formulas.pop()
                if ctx.utOperators().O_always() is not None: klass = Always
                elif ctx.utOperators().O_future() is not None: klass = Future
                elif ctx.utOperators().O_next() is not None: klass = Next
                else: raise Exception("Type error")
                self.formulas.append(klass(inner))
            else:
                raise Exception("Missing arguments")
        # Testing binary temporal operators
        elif ctx.btOperators() is not None:
            if len(self.formulas) > 1:
                f2 = self.formulas.pop()
                f1 = self.formulas.pop()
                if ctx.btOperators().O_until() is not None: klass = Until
                elif ctx.btOperators().O_release() is not None: klass = Release
                else: raise Exception("Type error")
                self.formulas.append(klass(f1, f2))
            else:
                raise Exception("Missing arguments")
        # Testing First order operators
        elif (ctx.uQuant() or ctx.eQuant()) is not None:
            ctx2 = ctx.uQuant() if ctx.uQuant() is not None else ctx.eQuant()
            klass = Forall if ctx.uQuant() is not None else Exists
            if len(self.formulas) > len(ctx2.vardec()):
                inner = self.formulas.pop()
                for x in range(len(ctx2.vardec())):
                    inner = klass(self.formulas.pop(), inner)
                self.formulas.append(inner)
            else:
                raise Exception("Missing arguments")

    def exitVardec(self, ctx:FODTLParser.VardecContext):
        vd = VarDec(str(ctx.ID()), str(ctx.vartype().ID()))
        self.formulas.append(vd)

    def exitNegation(self, ctx:FODTLParser.NegationContext):
        if len(self.formulas) > 0:
            inner = self.formulas.pop()
            self.formulas.append(Neg(inner))
        else:
            raise Exception("Missing arguments")

    def exitRemote(self, ctx:FODTLParser.RemoteContext):
        if len(self.formulas) > 0:
            inner = self.formulas.pop()
            self.formulas.append(At(str(ctx.ID()), inner))
        else:
            raise Exception("Missing arguments")

    def exitMain(self, ctx:FODTLParser.MainContext):
        if len(self.formulas) == 1:
            self.formula = self.formulas.pop()


    #######################
    # Parse
    #######################
    @staticmethod
    def parse(formula: str):
        f = InputStream(formula)
        lexer = FODTLLexer(f)
        stream = CommonTokenStream(lexer)
        parser = FODTLParser(stream)
        parser.addParseListener(FodtlParser())
        parser.buildParseTrees = True

        # TODO : important prediction mode optimization (we gain x5 speed up with SLL)
        # use SLL for the first pass, if an error detected we probably have to make a second pass
        # using LL mode (to check, see the doc)
        # parser._interp.predictionMode = PredictionMode.LL  # ~2.5
        parser._interp.predictionMode = PredictionMode.SLL  # ~0.4
        # parser._interp.predictionMode = PredictionMode.LL_EXACT_AMBIG_DETECTION  # ~2.5
        tr = parser.main()
        bt = Trees.toStringTree(tr, recog=parser)
        # print(bt)
        l = parser.getParseListeners().pop(0)
        return l.formula

