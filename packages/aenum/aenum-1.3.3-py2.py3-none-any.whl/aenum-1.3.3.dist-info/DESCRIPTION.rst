`aenum` includes the new Python stdlib enum module available in Python 3.4
backported for previous versions of Python from 2.7 and 3.3+
tested on 2.7, and 3.3+


An `Enum` is a set of symbolic names (members) bound to unique, constant
values.  Within an enumeration, the members can be compared by identity, and
the enumeration itself can be iterated over.

A `NamedTuple` is a class-based, fixed-length tuple with a name for each
possible position accessible using attribute-access notation.

A `NamedConstant` is a class whose members cannot be rebound;  it lacks all other
`Enum` capabilities, however; consequently, it can have duplicate values.
There is also a `module` function that can insert the `NamedConstant` class
into `sys.modules` where it will appear to be a module whose top-level
names cannot be rebound.


