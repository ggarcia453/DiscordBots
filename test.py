import random


class Test:
    def __init__(self, iterable: [(str, str)]):
        self.i = iterable

    def __iter__(self):
        self.i = iter(self.i)
        cont = True
        while cont:
            try:
                yield next(self.i)
            except StopIteration:
                cont = False

    def randomize(self):
        random.shuffle(self.i)
