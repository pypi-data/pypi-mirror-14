# -*- coding: utf-8 -*-

from requests.structures import LookupDict

_aggregates = {

    # Informational.
    'avg': ('avg',),
    'min': ('min',),
    'max': ('max',),
    'sum': ('sum',),
}

aggregates = LookupDict(name='aggregates')

for code, titles in _aggregates.items():
    for title in titles:
        setattr(aggregates, title, code)
        if not title.startswith('\\'):
            setattr(aggregates, title.upper(), code)
