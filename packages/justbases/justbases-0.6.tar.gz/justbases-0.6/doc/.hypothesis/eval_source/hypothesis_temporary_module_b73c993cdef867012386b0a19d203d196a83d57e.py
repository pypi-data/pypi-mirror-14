from hypothesis.utils.conventions import not_set

def accept(f):
    def testFromOther(self, nat=not_set, to_base=not_set):
        return f(self, nat, to_base)
    return testFromOther
