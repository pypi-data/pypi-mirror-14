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
from fodtlmon.fotl.fotlmon import *


def run_fotl_tests():
    pass

G(Forall(VD('x', 'w'), Neg(P('p(x)'))))
G(Imply(Exists(VD('x', 'w'), P('q(x)')), G(Forall(VD('y', 'w'), Neg(P('p(y)'))))))
# G A x:w.(s(x) && !r(x) && F r(x)) -> (!p(x) U r(x))
G(Forall(VD('x', 'w'), Imply(P('s(x)'), F(And(P('q(x)'), F(P('r(x)')))))))
# G A x:w.(s(x) && !p(x) && F p(x)) -> (u(x) U p(x))
# G A x:w.(n(x) && !p(x) && F p(x)) -> ((m(x) -> (!p(x) U (o(x) && !p(x)))) U p(x))
# G A x:w.q(x) -> ((!u(x) && !r(x)) U (r(x) || ((u(x) && !r(x)) U (r(x) || ((!u(x) && !r(x)) U (r(x) || ((u(x) && !r(x)) U (r(x) || (!u(x) W r(x)) || G u(x)))))))))
# G A x:w.(q(x) && !p(x)) -> (!p(x) U (E y:w.t(x,y) && !p(x)))