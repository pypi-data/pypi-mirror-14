# -*- coding:utf-8 -*-
import sys
import cssutils
from collections import defaultdict
VERBOSE = False


class Element(object):
    def __init__(self, sheet, structure=None, verbose=True, name=None):
        self.name = name
        self.sheet = sheet
        self.structure = structure or to_dict(self.sheet, verbose)
        self.verbose = verbose


def loads(css, verbose=VERBOSE, name=None):
    sheet = cssutils.parseString(css, validate=verbose)
    return Element(sheet, verbose=verbose, name=name)


def load(rf, verbose=VERBOSE):
    return loads(rf.read(), verbose=verbose, name=getattr(rf, "name", None))


def load_from_file(filename, verbose=VERBOSE):
    with open(filename) as rf:
        return load(rf)


def to_dict(sheet, verbose=True):
    d = defaultdict(lambda: defaultdict(list))
    for rule in sheet:
        if not hasattr(rule, "selectorList"):
            if verbose:
                sys.stderr.write("hmm: {}\n".format(type(rule)))
            continue
        for selector in rule.selectorList:
            sd = d[selector.selectorText]
            for prop in rule.style:
                sd[prop.name].append(prop.value)
    return d


def merge_element_to_dict(elements):
    d = defaultdict(lambda: defaultdict(list))
    for e in elements:
        for selector, child in e.structure.items():
            sd = d[selector]
            for name, values in child.items():
                sd[name].extend([(e.name, v) for v in values])
    return d


def detect_conflict(d):
    for selector, sd in sorted(d.items()):
        conflicted = []
        for name, values in sorted(sd.items()):
            if len(set(values)) > 1:
                conflicted.append((name, values))
        if conflicted:
            print("{selector} {{".format(selector=selector))
            for name, pairs in conflicted:
                for filename, value in pairs:
                    print("  {name}: {value}; /* {filename} */".format(name=name, value=value, filename=filename))
            print("}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=argparse.FileType('r'), nargs="+")
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()
    merged = merge_element_to_dict([load(f, verbose=args.verbose) for f in args.files])
    detect_conflict(merged)


if __name__ == "__main__":
    main()
