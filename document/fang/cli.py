from huffman_enc import Encode
from huffman_dec import Decode
from LZ_dec import lz78_decode
from LZ_enc import lz78_encode
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('way',type=str,
                    help='which code do you want to choose H or L')
parser.add_argument('op',type=str,
                    help='do you want to dec or enc')
parser.add_argument('source_path', type=str,
                    help='the file_path which you want to encode')
parser.add_argument('target_path', type=str, default=None,
                    help='the file_path which you want to output')


args = parser.parse_args()


try:
    if(args.way=='H'):
        if args.op=='enc':
            res = Encode.encode(source_path=args.source_path, target_path=args.target_path)
            print('\n{} has been encoded to {} in Huffman'.format(args.source_path, res))
        elif args.op=='dec':
            res = Decode.decode(source_path=args.source_path, target_path=args.target_path)
            print('\n{} has been decoded to {}'.format(args.source_path, res))
        else:
            print("can not understand op")
    elif(args.way=='L'):
        print()
    else:
        print("code way is not exist")
except FileNotFoundError as e:
    print(e)
except OSError as e:
    print(e)
    print('check your path!')
except Exception as e:
    print(e)
