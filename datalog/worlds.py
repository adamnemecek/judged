"""
Module responsible for possible world and descriptive sentence handling.
"""

from datalog import interned
from datalog import formatting


class Sentence:
    def evaluate(self, assignments):
        raise NotImplementedError

    def __format__(self, format_spec):
        return formatting.sentence(self, format_spec)

    def __repr__(self):
        return str(self, 'plain')

    def labels(self):
        return set()


class Binary(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def labels(self):
        return self.left.labels() | self.right.labels()


class Unary(Sentence):
    def __init__(self, sub):
        self.sub = sub

    def labels(self):
        return self.sub.labels()


class Atom(Sentence, metaclass=interned.InternalizeMeta):
    pass


class Disjunction(Binary):
    def __str__(self):
        return "({!s} or {!s})".format(self.left, self.right)

    def evaluate(self, assignments):
        return self.left.evaluate(assignments) or self.right.evaluate(assignments)


class Conjunction(Binary):
    def __str__(self):
        return "({!s} and {!s})".format(self.left, self.right)

    def evaluate(self, assignments):
        return self.left.evaluate(assignments) and self.right.evaluate(assignments)


class Negation(Unary):
    def __str__(self):
        return "not {!s}".format(self.sub)

    def evaluate(self, assignments):
        return not self.sub.evaluate(assignments)


class Label(Atom):
    def __init__(self, partitioning, part):
        self.partitioning = partitioning
        self.part = part

    def __str__(self):
        return "{}={}".format(self.partitioning, self.part)

    def evaluate(self, assignments):
        return assignments.check(self.partitioning, self.part)

    def labels(self):
        return set((self,))


class Top(Atom):
    def __str__(self):
        return "true"

    def evaluate(self, assignments):
        return True


class Bottom(Atom):
    def __str__(self):
        return "false"

    def evaluate(self, assignments):
        return False


def evaluate(sentence, assignments):
    """
    Evaluates a sentence for the given assignments.
    """
    return sentence.evaluate(assignments)
