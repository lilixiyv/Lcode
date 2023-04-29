from Huffman import Huffman


def encode(source_path, target_path):
    with open(source_path, 'rb') as fp_in:
        with open(target_path, 'wb') as fp_out:
            str_file = fp_in.read()
            if not str_file:  # 若为空文件，直接返回空文件
                return
            huffman = Huffman(str_file)

            write_buffer, huff_dic = huffman.encode()

            max_length = 0
            for code in huff_dic.values():
                max_length = max(max_length, len(code))
            length_lst = [0 for _ in range(max_length + 1)]
            for code in huff_dic.values():
                length_lst[len(code)] += 1
            # 要是256个字符全部位于同一层，使用全零标记
            if length_lst[max_length] == 256:
                length_lst[max_length] = 0
            length_lst.pop(0)  # 码长为0的字符并不存在，故删去
            code_bytes = b''.join(huff_dic.keys())  # 将所有字符按顺序（码长）存储
            length_bytes = b''.join(map(lambda x: bytes([x]), length_lst))  # 从码长为1开始，存每个码长对应的同码长字符数
            code_data = bytes([max_length]) + length_bytes + code_bytes
            write_buffer = code_data + write_buffer
            write_buffer = b'lxy' + write_buffer

            fp_out.write(write_buffer)


def decode(source_path, target_path):
    with open(source_path, 'rb') as fp_in:
        with open(target_path, 'wb') as fp_out:
            tmp_buffer = fp_in.read()
            if not tmp_buffer:
                return
            my_file = tmp_buffer[:3]
            buffer = tmp_buffer[3:]
            if my_file != b'lxy':
                return -1
            else:
                max_length = buffer[0]
                length = list(buffer[1:1 + max_length:])
                char_num = sum(length)  # 求层数
                # 如果length全零，那么表示256个字符全在同一层
                if char_num == 0 and max_length != 0:
                    char_num = 256
                    length[max_length - 1] = 256
                # 计算出还原huffman码表所需的信息
                char_lst, length_lst = [], []
                for pos in range(1 + max_length, 1 + max_length + char_num):
                    char_lst.append(bytes([buffer[pos]]))
                for i in range(max_length):
                    length_lst.extend([i + 1] * length[i])
                huff_dic = Huffman.rebuild(char_lst, length_lst)
                str_bytes = buffer[1 + max_length + char_num:]
                huffman = Huffman(str_bytes, huff_dic)
                write_buffer = huffman.decode()
                fp_out.write(write_buffer)
