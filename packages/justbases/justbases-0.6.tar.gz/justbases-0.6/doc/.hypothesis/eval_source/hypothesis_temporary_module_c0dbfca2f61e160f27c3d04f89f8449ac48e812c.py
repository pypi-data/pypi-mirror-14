from hypothesis.utils.conventions import not_set

def accept(f):
    def testFromOther(self, length=not_set, from_base=not_set, to_base=not_set):
        return f(self, length, from_base, to_base)
    return testFromOther
