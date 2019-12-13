import re

types = {
    "int": (int, r"[0-9\-]+"),
    "float": (float, r"[0-9\-]."),
    "str": (str, r"\w+")
}

class ReParse:
    def __init__(self, pattern, enclosers="{}"):
        self.typemap = {}
        self.patterntype = None
        self.numgroups = 0
        def replacer(g):
            patterntype = "dict" if g.group("name") else "tuple"
            assert self.patterntype == None or self.patterntype == patterntype, "All groups need to be either named or unnamed"
            self.patterntype = patterntype
            name = g.group("name") or f"g{self.numgroups}"
            self.numgroups += 1
            tp = g.group("typename")
            tpattern = types[tp][1]
            self.typemap[name] = types[tp][0]
            return f"(?P<{name}>{tpattern})"

        pre, post = [re.escape(c) for c in enclosers]
        self.pattern = re.sub(f'{pre}((?P<name>\\w+):)?(?P<typename>\\w+){post}', replacer, pattern)

    def map_match(self, mo):
        if mo:
            gs = mo.groupdict()
            if self.patterntype == "dict":
                return {
                    k: self.typemap[k](v)
                    for k, v in gs.items()
                }
            else:
                return tuple(self.typemap[n](gs[n]) for n in (f"g{i}" for i in range(self.numgroups)))

    def match(self, s):
        return self.map_match(re.match(self.pattern, s))
