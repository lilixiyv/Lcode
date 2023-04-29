import os
import hashlib


def file_hash(file_path: str) -> str:
    if not os.path.isfile(file_path):
        print('文件不存在。')
        return ''
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while b := f.read(8192):
            h.update(b)
    return h.hexdigest()


def test(path1, path2):
    hash1 = file_hash(path1)
    hash2 = file_hash(path2)
    print(f"\033[0;34m The sha256 of file1 is {hash1}\033[0m")
    print(f"\033[0;34m The sha256 of file2 is {hash2}\033[0m")
    if hash1 == hash2:
        print("\033[0;34m The hash value of the two files are the same!\033[0m")
    else:
        print("\033[0;31m The hash value of the two files are different!\033[0m")
