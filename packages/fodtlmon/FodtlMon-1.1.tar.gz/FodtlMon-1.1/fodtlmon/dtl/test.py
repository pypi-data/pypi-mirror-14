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
from fodtlmon.dtl.systemd import *
from fodtlmon.dtl.dtlmon import *


def run_dtl_tests():
    s = System()
    f1 = G(At(agent="alice", inner=F(P.parse("P(a)"))))
    # e = KVector.Entry("alice_b5bbaaef43512013e6319a76353c3d01", agent="alice", value=Boolean3.Bottom, timestamp=1)
    bob = Actor(name="bob", formula=f1, trace=Trace.parse("{P(a)}; {}"))
    f2 = G(F(P.parse("P(b)")))
    alice = Actor(name="alice", formula=f2, trace=Trace.parse("{P(a)}; {}"))
    s.add_actors([bob, alice])
    print(s)
    s.generate_monitors()
    print(s)
    print(s.get_actor("alice").submons[0].trace)
    s.run()
    print(s.get_actor("alice").monitor.KV)
    print(s.get_actor("bob").monitor.KV)
    # s.run()
    #print(s.get_actor("bob").monitor.monitor())
    System.parseJSON('{"actors": [  '
                     '{"name": "bob", "formula": "true()", "trace": "{}", "events": ["alice->"]}, '
                     '{"name": "alice", "formula": "true()", "trace": "{}", "events": ["->bob", ""] }'
                     ']}')
