from hypothesis.utils.conventions import not_set

def accept(f):
    def testFromInt(self, value=not_set, to_base=not_set):
        return f(self, value, to_base)
    return testFromInt
