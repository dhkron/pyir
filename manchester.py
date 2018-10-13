import sys
import itertools
import mode2reader
import electra


class Reader:
    I = 0
    O1 = 1
    O2 = 2
    O3 = 3
    Z1 = 4
    Z2 = 5
    R = 6
    R1 = 7
    R10 = 8
    R0 = 9
    R01 = 10

    labels = {
        I:    'Initial',
        O1:   'One 1',
        O2:   'Two 1',
        O3:   'Three 1',
        Z1:   'One 0',
        Z2:   'Two 0',
        R:    'Read start',
        R0:   'Read 0',
        R1:   'Read 1',
        R01:  'Read 01',
        R10:  'Read 10',
    }

    transition = {
        I:    [I,  O1],
        O1:   [I,  O2],
        O2:   [I,  O3],
        O3:   [Z1, O3],
        Z1:   [Z2, O1],
        Z2:   [R,  O1],
        R:    [R0, R1],
        R0:   [I,  R01],
        R1:   [R10,O2],
        R01:  [R0, R1],
        R10:  [R0, R1],
    }

    def __init__(
        self,
    ):
        self.s = self.I

    def read(
        self,
        stream,
    ):
        i = 0
        for bit in stream:
            prev_s = self.s
            self.s = self.transition[self.s][bit]
            i += 1
            #print(f'{i}: {self.labels[prev_s]}->{self.labels[self.s]}, b={bit}')

            if self.s == self.R01:
                yield 1
            if self.s == self.R10:
                yield 0
            if self.s == self.R:
                yield -1

    @classmethod
    def to_bytes(
        self,
        bits,
    ):
        c, b = None, None
        for bit in bits:
            if bit == -1:
                c, b = 0, 0
                continue

            b = b * 2 + bit
            if c == 7:
                yield b
                b = 0

            c = (c + 1) % 8

def chunk(iterable, n):
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


if __name__ == '__main__':
    wave = mode2reader.Reader.read_from_compact_file(
        path=sys.argv[1],
        rate=1000,
        start_is_space=bool(sys.argv[2]),
    )

    m = Reader()
    raw_bytes = Reader.to_bytes(
        bits=m.read(wave),
    )
    words = chunk(raw_bytes, 4)

    [print(electra.Code(list(word))) for word in words]

