from math import log2


class LZ78:
    """
    realize the encoding and decoding of LZ78 code
    need the path of input and output file
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def encode(self):
        with open(self.input_path, "rb") as f_in, open(self.output_path, "ab") as f_out:
            str_file_in = f_in.read()
            str_file = [bytes([c]) for c in str_file_in]
            dic_lz = {b'': 0}  # 存字典时没有必要存最后一个字符；key为当前字符串， value为最长前缀索引
            sub_dic = {b'': 0}  # 存索引与字符串关系
            len_dic = 1

            dic_lz[str_file[0]] = 0
            sub_dic[str_file[0]] = 1
            len_dic += 1
            f_out.write((0).to_bytes(1, byteorder='big'))
            f_out.write(str_file[0])
            str_file = str_file[1:]

            pre = b""
            for c in str_file:
                next_bytes = pre + c
                if next_bytes not in dic_lz:
                    l_num = int(log2(len_dic - 1) / 8) + 1
                    index = sub_dic[pre]
                    dic_lz[next_bytes] = index
                    sub_dic[next_bytes] = len_dic
                    len_dic += 1
                    f_out.write(index.to_bytes(l_num, 'big'))
                    f_out.write(c)
                    pre = b''
                else:
                    pre = next_bytes
            if pre != b'':
                l_num = int(log2(len_dic - 1) / 8) + 1
                index = sub_dic[pre]
                f_out.write(index.to_bytes(l_num, 'big'))

    def decode(self):
        with open(self.input_path, "rb") as f_in, open(self.output_path, "wb") as f_out:
            str_file = f_in.read()
            str_file = str_file[3:]
            len_file = len(str_file)
            dic_lz = {1: bytes([str_file[1]])}
            f_out.write(bytes([str_file[1]]))
            i = 2
            while i < len_file:
                len_dic = len(dic_lz)
                l_num = int(log2(len_dic) / 8) + 1
                if i + l_num >= len_file:
                    index = int.from_bytes(str_file[i:len_file], 'big')
                    last_char = b''
                    i += l_num

                else:
                    index = int.from_bytes(str_file[i:i+l_num], 'big')
                    last_char = bytes([str_file[i+l_num]])
                    i += (l_num+1)
                if index == 0:
                    dic_lz[len_dic+1] = last_char
                    f_out.write(last_char)
                else:
                    before = dic_lz[index]
                    bs = before + last_char
                    dic_lz[len_dic+1] = bs
                    f_out.write(bs)
