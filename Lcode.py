import sys
import argparse
from test import test
from En_De_code import huffman_encode, huffman_decode, lz78_decode, lz78_encode
sys.dont_write_bytecode = True

parser = argparse.ArgumentParser(
    prog='Lcode.py',
    description='file compressor and decompressor, using Huffman code or LZ78 code',
    usage='python Lcode.py [OPTION...]'
)
parser.add_argument('-i', '--input', type=str,
                    help='the absolute or relative path of the file to be processed')
parser.add_argument('-o', '--output', type=str, nargs="?", default="output",
                    help='the absolute or relative path of the file processed, the default name is \"output\"')
group1 = parser.add_mutually_exclusive_group()
group2 = parser.add_mutually_exclusive_group()
group1.add_argument('-c', '--compress', action="store_true",
                    help='compress the input file')
group1.add_argument('-d', '--decompress', action="store_true",
                    help='decompress the input file')
group2.add_argument('-H', '--Huffman', action='store_true',
                    help='use Huffman coding to compress or decompress the file')
group2.add_argument('-L', '--LZ', action='store_true',
                    help='use LZ coding to compress or decompress the file')
group2.add_argument('-T', '--hash_test', nargs=2, metavar=("file1", "file2"),
                    help='test the function of the coding by compare the hash value the file before compression and the one after decompression')

try:
    args = parser.parse_args()
    if not args.compress and not args.decompress and not args.hash_test:
        print("\033[0;31m [Lcode Error]Please choose the way to deal with the files!\033[0m")
        exit(0)
    if not args.input and not args.hash_test:
        print("\033[0;31m [Lcode Error]Please input the file that you want to compress or decompress!\033[0m")
        exit(0)
    if args.Huffman:
        if args.compress:
            huffman_encode(args.input, args.output)
            print("\033[0;32m \nthe {} has been compressed to {} with Huffman coding.\033[0m".format(args.input, args.output))
        if args.decompress:
            res = huffman_decode(args.input, args.output)
            if res == -1:
                print("\033[0;33m\nthe file is not compressed with Lcode!\033[0m".format(args.input, args.output))
                exit(0)
            print("\033[0;32m\nthe {} has been decompressed to {} with Huffman coding.\033[0m".format(args.input, args.output))
    elif args.LZ:
        if args.compress:
            lz78_encode(args.input, args.output)
            print("\033[0;32m \nthe {} has been compressed to {} with LZ78 coding.\033[0m".format(args.input, args.output))
        if args.decompress:
            res = lz78_decode(args.input, args.output)
            if res == -1:
                print("\033[0;33m\nthe file is not compressed with Lcode!\033[0m".format(args.input, args.output))
                exit(0)
            print("\033[0;32m\nthe {} has been decompressed to {} with LZ78 coding.\033[0m".format(args.input, args.output))
    elif args.hash_test:
        test(args.hash_test[0], args.hash_test[1])

    else:
        print("\033[0;31m [Lcode Error]Please choose the method to deal with the files!\033[0m")
        exit(0)

except Exception as e:
    print(f"\033[0;31m [Lcode Error]{e}\033[0m")
    exit(0)
