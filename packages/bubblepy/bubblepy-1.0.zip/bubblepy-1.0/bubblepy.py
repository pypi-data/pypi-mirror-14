import six


def get_byte(v):
    """If argument is integer, check if it fits into one byte. One-byte strings
    are first converted with ord()"""
    if isinstance(v, int):
        result = v
    else:
        result = ord(v)
    if not 0 < result < 255:
        raise ValueError('Non-ASCII character found. Encode your data')
    return result


class BubbleBabble(object):
    """ encodes or decodes to and from bubblebabble """
    def __init__(
            self, vowels='aeiouy', consonants='bcdfghklmnprstvzx', padding=None
        ):
        super(BubbleBabble, self).__init__()
        self.vowels = vowels
        self.consonants = consonants
        self.padding = padding or self.consonants[-1]

    def encode(self, src):
        out = self.padding
        c = 1

        for i in six.moves.range(0, len(src) + 1, 2):
            if i >= len(src):
                out += (
                    self.vowels[c % 6] +
                    self.consonants[16] +
                    self.vowels[c // 6]
                )
                break

            byte1 = get_byte(src[i])
            out += self.vowels[(((byte1 >> 6) & 3) + c) % 6]
            out += self.consonants[(byte1 >> 2) & 15]
            out += self.vowels[((byte1 & 3) + (c // 6)) % 6]

            if (i + 1) >= len(src):
                break

            byte2 = get_byte(src[i + 1])
            out += self.consonants[(byte2 >> 4) & 15]
            out += '-'
            out += self.consonants[byte2 & 15]

            c = (c * 5 + byte1 * 7 + byte2) % 36

        out += self.padding

        return out

    def decode(self, src):
        c = 1

        if src[0] != self.padding:
            raise ValueError(
                "corrupt string at offset 0: must begin with a '{}'".format(
                    self.padding
                )
            )

        if src[-1] != self.padding:
            raise ValueError(
                "corrupt string at the last offset: must end with a '{}'".\
                    format(self.padding)
            )

        if len(src) != 5 and len(src) % 6 != 5:
            raise ValueError("corrupt string: wrong length")

        src = src[1:-1]
        src = list(enumerate([src[x:x + 6] for x in range(0, len(src), 6)]))
        last_tuple = len(src) - 1
        out = bytes() 

        for k, tup in src:
            pos = k * 6
            tup = self._decode_tuple(tup, pos)

            if k == last_tuple:
                if tup[1] == 16:
                    if tup[0] != c % 6:
                        raise ValueError("corrupt string at offset %d (checksum)" % pos)

                    if tup[2] != int(c / 6):
                        raise ValueError("corrupt string at offset %d (checksum)" % (pos + 2))
                else:
                    byte = self._decode_3way_byte(tup[0], tup[1], tup[2], pos, c)
                    out += six.int2byte(byte)
            else:
                    byte1 = self._decode_3way_byte(tup[0], tup[1], tup[2], pos, c)
                    byte2 = self._decode_2way_byte(tup[3], tup[5], pos)

                    out += six.int2byte(byte1) + six.int2byte(byte2)

                    c = (c * 5 + byte1 * 7 + byte2) % 36

        return out

    def _decode_tuple(self, src, pos):
        tupl = [self.vowels.index(src[0]),
                self.consonants.index(src[1]),
                self.vowels.index(src[2])]
        try:
            tupl.append(self.consonants.index(src[3]))
            tupl.append('-')
            tupl.append(self.consonants.index(src[5]))
        except:
            pass

        return tupl

    def _decode_2way_byte(self, a1, a2, offset):
        if a1 > 16:
            raise ValueError("corrupt string at offset %d" % offset)

        if a2 > 16:
            raise ValueError("corrupt string at offset %d" % (offset + 2))

        return (int(a1) << 4) | int(a2)

    def _decode_3way_byte(self, a1, a2, a3, offset, c):
        high2 = (a1 - (c % 6) + 6) % 6

        if high2 >= 4:
            raise ValueError("corrupt string at offset %d" % offset)

        if int(a2) > 16:
            raise ValueError("corrupt string at offset %d" % (offset + 1))

        mid4 = a2
        low2 = (a3 - (c // 6 % 6) + 6) % 6

        if low2 >= 4:
            raise ValueError("corrupt string at offset %d" % (offset + 2))

        return high2 << 6 | mid4 << 2 | low2
