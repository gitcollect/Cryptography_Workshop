#!/usr/bin/env sage

import hashlib
import time

###########################################################
#
# Utility functions
#
###########################################################

def string2int(msg):
    # Warning: Trailing zeros ('\x00') are omitted!
    assert(msg[-1] != '\x00')
    msg = list(reversed(map(ord, list(msg))))
    m = msg[0]
    for c in msg[1:]:
        m = (m << 8) + c
    return(m)

def int2string(i):
    msg = []
    while(i > 0):
        msg += [chr(int(i) & 0xFF)]
        i = i >> 8
    return("".join(msg))


###########################################################
#
# One-way accumulator
#
###########################################################

n = 561508665948087545352987253256813938921L
referenceAccumulator = 230757756511379468965215489779427891997L

personalAccumulators = \
    [ ('Alice', 130436513274301151185661691739554173861L)
    , ('Bob', 266499640847330629410299179439453563206L)
    , ('Carol', 418929332127962703995790743851931669742L)
    , ('Eve', 479892121746869991037495826724031834611L)
    ]

def h(x, y, n):
    return pow(x, y, n)

# You suspect that one of the persons who claim to be members
# of the cabal is a snitch. In order to identify
# the snitch, you have to check their credentials.

def checkMembership(referenceAccumulator,
                    personalAccumulator,
                    person,
                    n):
    return referenceAccumulator == h(personalAccumulator, string2int(person), n)

# Now you know who is the snitch. Your next task is to provide
# fake credentials for the snitch. Calculate a personal accumulator
# for the snitch that passes the membership test!

def fakeCredentials(referenceAccumulator,
                    person,
                    n):
    return pow(referenceAccumulator, 1/string2int(person))

def findTheSnitch():
    for (person, acc) in personalAccumulators:
        if(not(checkMembership(referenceAccumulator=referenceAccumulator,
                               personalAccumulator=acc,
                               person=person,
                               n=n))):
            return(person)

if __name__ == "__main__":
    # Find the snitch
    snitch = findTheSnitch()
    assert(hashlib.sha256(snitch).hexdigest() ==
           'b9bae658d96579857efe22dee62673a31355446ddc6ad270ec046aa8c717081c')
    # Provide fake credentials for snitch
    fakeAccumulator = fakeCredentials(referenceAccumulator=referenceAccumulator,
                                      person=snitch,
                                      n=n)
    assert(checkMembership(referenceAccumulator=referenceAccumulator,
                          personalAccumulator=fakeAccumulator,
                          person=snitch,
                          n=n))
