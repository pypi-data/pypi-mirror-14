from constants import *


def merge(first, second):
    return first + list(set(second) - set(first))


def intersect(first, second):
    return list(set(first).intersection(second))


def get_attribute(obj, attr, default=None):
    result = obj
    comparison = None
    parts = attr.split('__')

    for p in parts:
        if result is None:
            break
        elif p in COMPARISONS:
            comparison = p
        else:
            result = getattr(result, p, None)

    value = result if result != obj else default
    return value, comparison


def is_match(first, second, comparison):
    if not comparison:
        return first == second
    return {
        COMPARISON_EXACT: first.lower() == second.lower()
    }[comparison]


def matches(*source, **attrs):
    exclude = []
    for x in source:
        for key, value in attrs.items():
            if not is_match(value, *get_attribute(x, key)):
                exclude.append(x)
                break
    for x in source:
        if x not in exclude:
            yield x
