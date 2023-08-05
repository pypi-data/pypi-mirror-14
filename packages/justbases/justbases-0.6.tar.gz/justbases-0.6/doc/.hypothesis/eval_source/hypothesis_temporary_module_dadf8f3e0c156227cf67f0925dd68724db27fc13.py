from hypothesis.utils.conventions import not_set

def accept(f):
    def testCarryIn(self, value=not_set, carry=not_set):
        return f(self, value, carry)
    return testCarryIn
