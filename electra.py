class Code:
    cmd_labels = {
        0b0: 'SET',
        0b1: 'ON/OFF',
    }
    mode_labels = {
        0b000: 'TIMER',
        0b001: 'COOL',
        0b010: 'HEAT',
        0b011: 'TRIANGLE',
        0b100: 'DROPLET',
        0b101: 'FAN',
        0b110: '?110',
        0b111: '?111',
    }
    fan_labels = {
        0: '*   ',
        1: '**  ',
        2: '*** ',
        3: '*A* ',
    }
    swing_labels = {
        0: 'no  ',
        1: 'mini',
        2: 'auto',
        3: '?   ',
    }

    def __init__(
        self,
        word,
    ):
        self.turn_on    =  (word[0] & 0b10000000) >> 7
        self.mode       =  (word[0] & 0b01110000) >> 4
        self.fan_speed  =  (word[0] & 0b00001100) >> 2
        self.unk1       =  (word[0] & 0b00000010) >> 1
        self.mini_swing =  (word[0] & 0b00000001) >> 0
        self.auto_swing =  (word[1] & 0b10000000) >> 7
        self.unk2       =  (word[1] & 0b01100000) >> 5
        self.temp       = ((word[1] & 0b00011110) >> 1) + 0b1111
        self.sleep      =  (word[1] & 0b00000001) >> 0
        self.raw        = word

    def __str__(
        self,
    ):
        return '<'\
                f'{self.cmd_labels[self.turn_on]}'\
                f' {self.mode_labels[self.mode]}'\
                f' {self.fan_labels[self.fan_speed]}'\
                f' swing={self.swing_labels[self.mini_swing + 2*self.auto_swing]}'\
                f' {self.temp}°'\
                f' sleep={self.sleep}'\
                f' unk1={self.unk1}'\
                f' unk2={self.unk2}'\
                f' raw3={pbin(self.raw[2])}'\
                f' raw4={pbin(self.raw[3])}'\
                '>'


def pbin(
    b,
):
    return bin(b)[2:].zfill(8)
