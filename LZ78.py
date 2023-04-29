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
        str_file = open(self.input_path, "rb").read()
        f_out = open(self.output_path, "wb")
        len_file = len(str_file)
        dic_lz = {bytes([str_file[0]]): 0}
        f_out.write(b'lxy')  # 标记自己的文档
        f_out.write((0).to_bytes(1, byteorder='big'))
        f_out.write(bytes([str_file[0]]))
        for i in range(1, len_file):
            print(dic_lz)
            len_dic = len(dic_lz)

            l_num = int(len_dic.bit_length() / 8) + 1
            end = 0  # 需要标记是否已经处理完
            pre = bytes([str_file[i]])
            value = LZ78._max_find(pre, dic_lz)  # 预处理避免出错
            tmp = value
            while value != -1:
                i += 1
                if i == len_file:
                    end = 1
                    break
                tmp = value
                pre += bytes([str_file[i]])
                value = LZ78._max_find(pre, dic_lz)
            if end == 1:
                f_out.write(value.to_bytes(l_num, 'big'))
            else:
                i += 1
                if tmp == -1:
                    dic_lz[pre] = 0
                    f_out.write((0).to_bytes(l_num, 'big'))
                    f_out.write(bytes([pre[-1]]))
                else:
                    dic_lz[pre] = len_dic + 1
                    f_out.write(tmp.to_bytes(l_num, 'big'))
                    f_out.write(bytes([pre[-1]]))

    def decode(self):
        str_file = open(self.input_path, "rb").read()
        f_out = open(self.output_path, "wb")
        dic_lz = {}
        my_file = str_file[:3]
        str_file = str_file[3:]
        len_file = len(str_file)
        if my_file != b'lxy':
            return -1
        i = 0
        while i < len_file:
            print(dic_lz)
            len_dic = len(dic_lz)
            if len_dic == 0:
                l_num = 1
            else:
                l_num = int(len_dic.bit_length()/8) + 1
            index = int.from_bytes(str_file[i:i+l_num], 'big')
            print(i+l_num, len_file)
            if i + l_num == len_file:
                last_char = b''
            else:
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
