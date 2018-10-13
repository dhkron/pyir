import sys


class Reader:
    def __init__(
        self,
        rate,
        start_is_space,
    ):
        self.rate = rate
        if start_is_space:
            self.bit = 0
        else:
            self.bit = 1

    def read(
        self,
        wave,
    ):
        for duration in wave:
            units = round(duration/self.rate)

            yield from [self.bit]*units

            self.bit = 1-self.bit

    @classmethod
    def read_from_compact_file(
        cls,
        path,
        rate,
        start_is_space,
    ):
        r = Reader(
            rate=rate,
            start_is_space=start_is_space,
        )
        with open(path, 'r') as f:
            for line in f.readlines():
                values = line.strip().split(' ')

                yield from r.read(
                    wave=[
                        int(value.strip())
                        for value in values
                        if len(value.strip()) > 0
                    ],
                )

    @classmethod
    def read_from_verbose_file(
        cls,
        path,
        rate,
        start_is_space,
    ):
        raise NotImplementedError()


if __name__ == '__main__':
    wave = Reader.read_from_compact_file(
        path=sys.argv[1],
        rate=1000,
        start_is_space=bool(sys.argv[2]),
    )

    print(list(wave))
