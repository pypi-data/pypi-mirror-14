"""
dtl
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
from hashlib import md5


#############################
# Localisation Operators
#############################

class At(UExp):
    """
    Localisation operator
    """
    symbol = "@"

    def __init__(self, agent="", inner=None, fid=-1):
        super().__init__(inner)
        self.agent = agent
        self.fid = fid

    def toTSPASS(self):
        raise Exception("Not compatible with TSPASS !")

    def toLTLFO(self):
        raise Exception("Not compatible with TSPASS !")

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.agent, self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "@_{%s}(%s)" % (self.agent, self.inner)

    def compute_hash(self, sid=""):
        # TODO : if called after init pb with mon rewrite
        self.fid = "%s@%s_%s" % (sid, self.agent, md5(str(self.inner).encode()).hexdigest())


#############################
# Knowledge vectors
#############################

class IKVector:
    """
    KVector interface
    """
    class Entry:
        def __init__(self, fid, agent="", value=Boolean3.Unknown, timestamp=0):
            self.fid = fid
            self.agent = agent
            self.value = value
            self.timestamp = timestamp

        def __str__(self):
            # return "{fid:%s; agent:%s; value:%s; timestamp:%s}" % (self.fid, self.agent, self.value, self.timestamp)
            return "{%s; %s; %s; %s}" % (self.fid, self.agent, self.value, self.timestamp)

        def time_compare(self, other):
            if self.fid == other.fid and self.agent == other.agent:
                if self.timestamp == other.timestamp: return 0
                elif self.timestamp > other.timestamp: return 1
                else: return -1
            else:
                return None

        def update(self, e):
            self.fid = e.fid
            self.agent = e.agent
            self.value = e.value
            self.timestamp = e.timestamp

        @classmethod
        def parse(cls, string: str):
            res = None
            if string.startswith("{") and string.endswith("}"):
                elems = string[1:-1].split(";")
                if len(elems) > 3:
                    res = IKVector.Entry(elems[0], agent=elems[1], value=B3(elems[2]), timestamp=int(elems[3]))
            return res

    def __init__(self, entries=None):
        self.entries = [] if entries is None else entries

    def add_entry(self, entry):
        raise Exception("Unimplemented method !")

    def has(self, entry):
        raise Exception("Unimplemented method !")

    def get_entry(self, entry):
        raise Exception("Unimplemented method !")

    def update(self, entry):
        raise Exception("Unimplemented method !")

    @classmethod
    def parse(cls, vector):
        raise Exception("Unimplemented method !")


class KVector(IKVector):
    """
    Knowledge vector
    """

    def __str__(self):
        return ",".join([str(e) for e in self.entries])

    def has(self, entry):
        if isinstance(entry, KVector.Entry):
            return next((self.entries.index(x) for x in self.entries if x.fid == entry.fid), -1)
        else:
            return next((self.entries.index(x) for x in self.entries if x.fid == entry), -1)

    def update(self, entry):
        # i = self.has(entry)
        i = self.get_entry(entry)
        if i is not None:
            if entry.time_compare(i) == 1:
                i.update(entry)
        else:  # Add it
            self.add_entry(entry)

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_entry(self, entry):
        if isinstance(entry, IKVector.Entry):
            return next((x for x in self.entries if x.fid == entry.fid), None)
        else:
            return next((x for x in self.entries if x.fid == entry), None)

    @classmethod
    def parse(cls, vector):
        res = KVector()
        entries = vector.split(",")
        for e in entries:
            tmp = IKVector.Entry.parse(e)
            if tmp is not None:
                res.entries.append(tmp)
        return res


class KVector_H(KVector):
    """
    Knowledge vector second implementation
    """
    def __init__(self, entries=None):
        self.entries = {} if entries is None else entries

    def __str__(self):
        return ",".join([",".join([str(x) for x in self.entries[e]]) for e in self.entries])

    def add_entry(self, entry):
        e = self.entries.get(entry.agent)
        if e is None:
            self.entries[entry.agent] = [entry]
        else:
            self.entries[entry.agent].append(entry)

    def has(self, entry):
        if isinstance(entry, KVector_H.Entry):
            e = self.entries.get(entry.agent)
            if e is None:
                return -1
            else:
                return next((e.index(x) for x in e if x.fid == entry.fid), -1)
        return -1

    def get_entry(self, entry):
        if isinstance(entry, IKVector.Entry):
            e = self.entries.get(entry.agent)
            if e is None: return e
            return next((x for x in e if x.fid == entry.fid), None)
        else:
            n = entry.split("_")[0]
            e = self.entries.get(n)
            if e is None: return e
            x = next((x for x in e if x.fid == entry), None)
            return x

