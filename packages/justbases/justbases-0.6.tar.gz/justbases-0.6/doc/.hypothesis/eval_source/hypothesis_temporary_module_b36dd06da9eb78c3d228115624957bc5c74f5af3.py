from hypothesis.utils.conventions import not_set

def accept(f):
    def testCarryIn(self, strategy=not_set):
        return f(self, strategy)
    return testCarryIn
