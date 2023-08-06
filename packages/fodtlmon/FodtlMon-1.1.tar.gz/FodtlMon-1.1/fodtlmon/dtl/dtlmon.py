"""
dtlmon DTL monitor
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
from fodtlmon.dtl.dtl import *
from fodtlmon.ltl.ltlmon import *


class Dtlmon(Ltlmon):
    """
    DTL monitor using progression technique
    """
    def __init__(self, formula, trace, actor=None, parent=None, fid=""):
        super().__init__(formula, trace)
        self.KV = KVector()
        self.actor = actor
        self.last = Boolean3.Unknown
        self.parent = self if parent is None else parent
        self.fid = fid
        self.rewrite = copy.deepcopy(self.formula)

    def prg(self, formula, event, valuation=None):
        if isinstance(formula, At):
            # Check in KV
            res = self.KV.get_entry(formula.fid)
            # return Boolean3.Unknown if res == -1 else self.get_kv().entries[res].value
            # x = self.get_kv().entries[res].value
            # TODO add check
            x = res.value
            if x is Boolean3.Unknown:
                return formula
            elif x is Boolean3.Top:
                return true()
            else:
                return false()
        elif isinstance(formula, Boolean3):
            return formula
        else:
            return super().prg(formula, event, valuation)

    def get_kv(self):
        return self.parent.KV

    def get_trace(self):
        return self.parent.trace

    def update_kv(self, kv: IKVector):
        for e in kv.entries:
            self.KV.update(e)
