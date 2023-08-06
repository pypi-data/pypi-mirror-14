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
from fodtlmon.dtl.dtlmon import *
from fodtlmon.fotl.fotlmon import *


class Fodtlmon(Dtlmon, Fotlmon):
    """
    Fodtl monitoring using progression technique
    """

    def __init__(self, formula, event, actor=None, parent=None, fid=""):
        Dtlmon.__init__(self, formula, event, actor=actor, parent=parent, fid=fid)

    def prg(self, formula, event, valuation=None):
        if isinstance(formula, Forall) or isinstance(formula, Predicate) or isinstance(formula, ForallConj):
            return Fotlmon.prg(self, formula, event, valuation)
        else:
            return Dtlmon.prg(self, formula, event, valuation)
