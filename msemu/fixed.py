import logging, sys
from math import log, ceil, floor, log2

class Binary:
    def __init__(self, n):
        self.n = n

    def bin_str(self, val):
        if val < 0:
            conv_val = (1 << self.n) + val
        else:
            conv_val = val

        str_val = format(conv_val, '0' + str(self.n) + 'b')
        if len(str_val) != self.n:
            raise ValueError('Value to be converted cannot be represented: %d, %d' % (val, self.n))

        return str_val

class Unsigned(Binary):
    @property
    def min(self):
        return 0

    @property
    def max(self):
        return (1<<self.n)-1

    @staticmethod
    def get_bits(val):
        return int(ceil(log2(val+1)))

class Signed(Binary):
    @property
    def min(self):
        return -(1<<(self.n-1))

    @property
    def max(self):
        return (1<<(self.n-1))-1

    @staticmethod
    def get_bits(val):
        if val < 0:
            return int(ceil(1 + log2(-val)))
        else:
            return int(ceil(1 + log2(val+1)))

class Fixed:
    def __init__(self, point):
        self.point = point

    @property
    def res(self):
        return Fixed.point2res(self.point)

    def float2fixed(self, val, mode='round'):
        return Fixed.intval(val=val, point=self.point, mode=mode)

    @staticmethod
    def res2point(res):
        return int(ceil(-log2(res)))

    @staticmethod
    def point2res(point):
        return 2.0 ** (-point)

    @staticmethod
    def intval(val, point, mode='round'):
        scaled = val/Fixed.point2res(point)

        if mode.lower() in ['round']:
            return int(round(scaled))
        elif mode.lower() in ['ceil']:
            return int(ceil(scaled))
        elif mode.lower() in ['floor']:
            return int(floor(scaled))
        else:
            raise ValueError('Invalid truncation mode.')

class FixedUnsigned(Fixed, Unsigned):
    def __init__(self, n, point):
        Fixed.__init__(self, point=point)
        Unsigned.__init__(self, n=n)

    def bin_str(self, val):
        return Unsigned.bin_str(self, self.float2fixed(val))

    @staticmethod
    def get_format(val, res):
        point=Fixed.res2point(res)
        fixed = Fixed.intval(val=val, point=point)
        n = Unsigned.get_bits(fixed)

        return FixedUnsigned(n=n, point=point)

class FixedSigned(Fixed, Signed):
    def __init__(self, n, point):
        Fixed.__init__(self, point=point)
        Signed.__init__(self, n=n)

    def bin_str(self, val):
        return Signed.bin_str(self, self.float2fixed(val))

    @staticmethod
    def get_format(val, res):
        point=Fixed.res2point(res)
        fixed = Fixed.intval(val=val, point=point)
        n = Signed.get_bits(fixed)

        return FixedSigned(n=n, point=point)

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    fmt = FixedSigned.get_format(1.23, 0.0001)
    print(fmt.bin_str(-0.456))

if __name__=='__main__':
    main()
