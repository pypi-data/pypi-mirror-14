"""
systemd
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
import json
import copy
from fodtlmon.tools.color import *

#############################
# System Actor
#############################
class Actor:
    """
    Actor class
    """

    class Event:
        """
        Internal actor event
          in  : actor-> event coming from actor
          out : ->actor sending event to actor
        """
        class EventType(Enum):
            IN = "in",
            OUT = "out"
            EMPTY = "EMPTY"

        def __init__(self, target="", e_type=EventType.EMPTY):
            self.target = target
            self.e_type = e_type

        def __str__(self):
            if self.e_type is Actor.Event.EventType.IN:
                return "%s->" % self.target
            elif self.e_type is Actor.Event.EventType.OUT:
                return "->%s" % self.target
            else:
                return "->"

        @staticmethod
        def parse(ste):
            ste = ste.strip()
            if ste == "" or ste == "->":
                return Actor.Event(e_type=Actor.Event.EventType.EMPTY)
            else:
                res = ste.split("->")
                if len(res) < 2:
                    raise Exception("Malformed Actor internal event !")
                if res[0] == "":
                    return Actor.Event(target=res[1], e_type=Actor.Event.EventType.OUT)
                else:
                    return Actor.Event(target=res[0], e_type=Actor.Event.EventType.IN)

    def __init__(self, name="", formula=None, trace=None, events=None, speed=1):
        self.name = name
        self.formula = formula
        self.trace = trace
        self.monitor = None
        self.submons = []
        self.events = [] if events is None else events
        self.speed = speed

    def __str__(self):
        evs = "[%s]" % ",".join(str(e) for e in self.events)
        return "{%s; %s; %s; %s; %s; %s}" % (self.name, self.formula, self.trace, self.monitor, self.submons, evs)

    def update_kv(self, kv):
        """
        Update the KV of the main monitor
        :param kv:
        :return:
        """
        self.monitor.update_kv(kv)

    def get_kv(self):
        return self.monitor.get_kv()

    def run(self, once=True):
        """
        Run main monitor and all sub monitors
        :param : once
        :return:
        """
        print("\n- Actor %s " % self.name)
        for m in self.submons:
            res = m.monitor(once=once)
            print("   | Submonitor %s : %s" % (self.name, res))
            # print("%s %s %s %s lst %s" % (self.name, m.fid, m.last, m.counter, m.last))
            self.get_kv().update(KVector.Entry(m.fid, agent=self.name, value=m.last, timestamp=m.counter))
        res = self.monitor.monitor(once=once)
        print("  Main monitor %s : %s" % (self.name, res))
        # print(self.get_kv())

    def push_event(self, event):
        self.monitor.push_event(event)


#############################
# Distributed system
#############################
class System:
    """
    Distributed system representation
    """
    def __init__(self, actors=None, kv_implementation=KVector):
        """
        Init the system
        coms is a dictionary that contains
        :param actors: actors list
        :param kv_implementation: the Knowledge vector implementation (IKVector)
        :return:
        """
        self.actors = [] if actors is None else actors
        self.mons = []
        self.turn = 0
        self.kv_implementation = kv_implementation
        self.coms = {}

    def __str__(self):
        return " | ".join([str(a) for a in self.actors])

    def add_actors(self, actor):
        """
        Add an actor / actor list to the system's actors
        :param actor: Actor | list<Actor>
        :return: self
        """
        if isinstance(actor, list):
            self.actors.extend(actor)
        elif isinstance(actor, Actor):
            self.actors.append(actor)
        return self

    def get_actor(self, name):
        """
        Get an actor by name
        :param name: str
        :return:
        """
        return next((x for x in self.actors if x.name == name), None)

    def generate_monitors(self):
        """
        Generate monitors for each actor in the system
        :return:
        """
        submons = []
        for a in self.actors:
            # Get all remote formula
            remotes = a.formula.walk(filter_type=At)
            # Compute formula hash
            for f in remotes:
                f.compute_hash(sid=a.name)

            # Create the global monitor for the actor
            a.monitor = Dtlmon(a.formula, a.trace)

            # Create the remote sub monitors for each @Formula
            for f in remotes:
                remote_actor = self.get_actor(f.agent)
                remote_actor.submons.append(Dtlmon(formula=f.inner, trace=remote_actor.trace, parent=remote_actor.monitor, fid=f.fid))
                submons.append({"fid": f.fid, "actor": remote_actor.name})

            # Create the com entry in the system
            for a2 in self.actors:
                self.coms["%s->%s" % (a.name, a2.name)] = []
                self.coms["%s->%s" % (a2.name, a.name)] = []

        # Create the general KV structure
        kv = self.kv_implementation()
        for m in submons:
            kv.add_entry(self.kv_implementation.Entry(m["fid"], agent=m["actor"], value=Boolean3.Unknown, timestamp=0))

        # Add a copy of KV structure for each actor
        for a in self.actors:
            a.monitor.KV = copy.deepcopy(kv)

    def run(self, once=True):
        """
        Run the system
        :param once
        :return:
        """
        print(Color("{autored}\n====== System round %s ======{/red}" % self.turn))
        print(Color("{autoblue}== Updating actors events...{/blue}"))
        # Handling OUT messages
        for a in self.actors:
            if self.turn < len(a.events):
                es = a.events[self.turn]
                for e in es:
                    if e.e_type == Actor.Event.EventType.OUT:
                        # register
                        # print("Sending from %s to %s %s" % (a.name, e.target, a.get_kv()))
                        if e.target is "*":
                            print("Broadcasting")
                            for ac in self.actors:
                                self.coms["%s->%s" % (a.name, ac.name)].append(copy.deepcopy(a.get_kv()))
                        else:
                            self.coms["%s->%s" % (a.name, e.target)].append(copy.deepcopy(a.get_kv()))

        # Handling IN messages
        for a in self.actors:
            if self.turn < len(a.events):
                es = a.events[self.turn]
                for e in es:
                    if e.e_type == Actor.Event.EventType.IN:
                        # Update KV and check pop the send
                        print("%s received a message from %s ..." % (a.name, e.target))
                        if len(self.coms["%s->%s" % (e.target, a.name)]) > 0:
                            a.update_kv(self.coms["%s->%s" % (e.target, a.name)].pop(0))
                            print(" - IN %s %s" % (a.name, a.get_kv()))
                        else:
                            print(" - Error %s trying to receive a message from %s that was not sent by %s" % (a.name, e.target, e.target))

        print(Color("{autoblue}\n== Running monitors on each actor...{/blue}"))
        for a in self.actors:
            for i in range(a.speed):
                a.run(once=once)
        self.turn += 1

    def update_events(self, e):
        """
        Update KV of each actor
        :param e:
        :return:
        """
        for a in self.actors:
            a.update_kv(e)

    @staticmethod
    def parseJSON(js):
        """
        {
            kv_type : "",
            type    : "",
            actors  : <Actors list>
                [
                    {
                     actorName : <String>,
                     formula: <String>,
                     events: ["->b", "b->"],
                     trace: [],
                     speed: 1,2,3...
                    }
                ]
        }
        :param json:
        :return:
        """
        decoded = json.JSONDecoder().decode(js)
        actors = decoded.get("actors")
        if actors is None:
            raise Exception("No actors found in the system !")
        s = System()
        for a in actors:
            # Getting actor info
            a_name = a.get("name")
            a_formula = a.get("formula")
            a_trace = a.get("trace")
            sa_events = a.get("events")
            a_events = []
            a_speed = 1 if a.get("speed") is None else int(a["speed"])

            # Parsing actor info
            for e in sa_events:
                tmp = e.split("|")
                tmp2 = []
                for x in tmp:
                    tmp2.append(Actor.Event.parse(x))
                a_events.append(tmp2)
            a_formula = eval(a_formula)
            a_trace = Trace.parse(a_trace)

            # Creating the actor
            actor = Actor(name=a_name, formula=a_formula, trace=a_trace, events=a_events, speed=a_speed)

            # Add actor to the system
            s.add_actors(actor)
        s.generate_monitors()
        return s
