import png
import sys



def string_to_png(string, output):
    string = string.encode('utf-16be')
    png.from_array([string], 'L').save(output)

def png_to_string(file):
    pixels = png.Reader(file).read_flat()[2]
    pixels = list(map(chr, pixels))
    return b''.join(pixels).decode('utf-16be')

if __name__ == '__main__':
    if sys.argv[1] == 'encode':
        with open( sys.argv[3], 'wb') as  output:
            string_to_png(sys.argv[2], output)
    else:
        with open( sys.argv[2], 'rb') as file:
            result = png_to_string(file)
            print(result)