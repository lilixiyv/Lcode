from math import log2


class LZ78:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @staticmethod
    def _max_find(bts, dic):
        i = 1
        for key in dic:
            if bts == key:
                return i
            i += 1
        return -1

    def encode(self):
        with open(self.input_path, "rb") as f_in, open(self.output_path, "wb") as f_out:
            str_file = f_in.read()
            len_file = len(str_file)
            dic_lz = {bytes([str_file[0]]): 0}  # 存字典时没有必要存最后一个字符
            sub_dic = [bytes([str_file[0]])]
            f_out.write(b'lxy')  # 标记自己的文档
            f_out.write((0).to_bytes(1, byteorder='big'))
            f_out.write(bytes([str_file[0]]))
            i = 1
            while i < len_file:
                len_dic = len(dic_lz)
                l_num = int(log2(len_dic)/8) + 1
                end_flag = 0  # 需要标记是否已经处理完
                now = b''
                pre = bytes([str_file[i]])
                while pre in dic_lz:
                    i += 1
                    if i == len_file:
                        end_flag = 1
                        break
                    now = pre
                    pre += bytes([str_file[i]])
                if end_flag == 1:
                    index = sub_dic.index(pre) + 1
                    f_out.write(index.to_bytes(l_num, 'big'))
                else:
                    if now == b'':
                        index = 0
                    else:
                        index = sub_dic.index(now) + 1
                    dic_lz[pre] = index
                    sub_dic.append(pre)
                    f_out.write(index.to_bytes(l_num, 'big'))
                    f_out.write(bytes([str_file[i]]))
                    i += 1

    def decode(self):
        str_file = open(self.input_path, "rb").read()
        f_out = open(self.output_path, "wb")
        my_file = str_file[:3]
        str_file = str_file[3:]
        len_file = len(str_file)
        if my_file != b'lxy':
            return -1
        dic_lz = {1: bytes([str_file[1]])}
        f_out.write(bytes([str_file[1]]))
        i = 2
        while i < len_file:
            len_dic = len(dic_lz)

            l_num = int(log2(len_dic) / 8) + 1
            if i + l_num >= len_file:
                index = int.from_bytes(str_file[i:len_file], 'big')
                last_char = b''
                print(i + l_num == len_file)
                print(str_file[i:len_file])
                i += l_num
                print(index)

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
