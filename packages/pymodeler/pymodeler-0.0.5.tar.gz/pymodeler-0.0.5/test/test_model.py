#!/usr/bin/env python
"""
Test the model build
"""
from pymodel import Model
from pymodel import Param

class Parent(Model):
    _params = (
        ('x', Param(1)              , 'variable x'),
        ('y', Param(2,bounds=[0,10]), 'variable y'),
    )

class Child(Parent):
    _params = Parent._params + (
        ('z', Param(None), 'variable z'),
    )

    _mapping = (
        ('zed','z'),
    )

if __name__ == "__main__":
    import argparse
    description = __doc__
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    a = Parent()
    print a

    a.x = 3
    a.y = 4
    print a

    b = Child()
    print b
    for k,v in a.params.items():
        b.setp(k,v)
    b.z = 100
    print b
