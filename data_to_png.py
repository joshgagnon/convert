import png
import sys
from functools import reduce


def string_to_png(string, output):
    string = string.encode('utf-16be')
    while len(string) % 3 != 0:
        string += ' '.encode('utf-16be')
    # make every 4th byte 0
    string = reduce(lambda x, y: x + list(y) + [0], list(zip(*[iter(string)] * 3)), [])
    png.from_array([string], 'RGBA').save(output)

def png_to_string(file):
    pixels = png.Reader(file).read_flat()[2]
    # remove every 4th byte
    pixels = reduce(lambda x, y: x + list(y)[:3], list(zip(*[iter(pixels)] * 4)), [])
    return bytearray(pixels).decode('utf-16be')


if __name__ == '__main__':
    if sys.argv[1] == 'encode':
        with open( sys.argv[3], 'wb') as  output:
            string_to_png(sys.argv[2], output)
    else:
        with open( sys.argv[2], 'rb') as file:
            result = png_to_string(file)
            print(result)