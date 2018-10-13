class Code:
    cmd_to_str = {
        0b000101: 'SET',
        0b001101: 'ON/OFF',
    }

    def __init__(
        self,
        word,
    ):
        self.cmd = (word[0] & 0b1111110000) >> 4 # Command contains some more stuff atm
        self.fan_speed = (word[0] & 0b1100) >> 2
        self.temp = ((word[1] & 0b11110) >> 1) + 0b1111

    def __str__(
        self,
    ):
        return f'{self.cmd_to_str[self.cmd]} temp={self.temp} speed={self.fan_speed}'
