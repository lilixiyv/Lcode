from Huffman import int2bytes, huffman


class Decode:
    @classmethod
    def decode_as_huffman(cls, bts):
        padding = bts[0]
        max_length = bts[1]
        length = list(bts[2:2 + max_length:])
        char_num = sum(length)#求层数
        # 如果length全零，那么表示256个字符全在同一层
        if char_num == 0 and max_length != 0:
            char_num = 256
            length[max_length - 1] = 256
        # 计算出还原huffman码表所需的信息
        char_lst, length_lst = [], []
        for pos in range(2 + max_length, 2 + max_length + char_num):
            char_lst.append(int2bytes(bts[pos]))
        for i in range(max_length):
            length_lst.extend([i + 1] * length[i])
        code_dic = huffman.rebuilt(char_lst,length_lst)
        str_bytes = bts[2 + max_length + char_num:]
        write_buffer = huffman.decode(str_bytes, code_dic, padding)
        return write_buffer

    @classmethod
    def decode(cls, source_path, target_path):
        with open(source_path, 'rb') as fp_in:
            with open(target_path, 'wb') as fp_out:
                tmp_buffer=fp_in.read()
                myfile=tmp_buffer[:3]
                buffer =tmp_buffer[3:]
                if myfile!=b'bdm':
                    print("this is not my file")
                    return None
                else:
                    write_buffer = cls.decode_as_huffman(buffer)
                    fp_out.write(write_buffer)

        return target_path
