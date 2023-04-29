from Huffman import Huffman


def int2bytes(n: int) -> bytes:  # maybe no need for such a special function
    """
    turn a number (which is the ASCII code of a character) to bytes
    :param n: int
    :return bytes_n : bytes
    """
    return bytes([n])  # 将acs码值转化为bytes串


def encode(source_path, target_path):
    with open(source_path, 'rb') as fp_in:
        with open(target_path, 'wb') as fp_out:
            str_file = fp_in.read()
            if not str_file:
                return
            huffman = Huffman(str_file)

            write_buffer, huff_dic, padding = huffman.encode()

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
            code_bytes = b''.join(huff_dic.keys())
            length_bytes = b''.join(map(int2bytes, length_lst))
            code_data = int2bytes(max_length) + length_bytes + code_bytes
            write_buffer = int2bytes(padding) + code_data + write_buffer
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
                padding = buffer[0]
                max_length = buffer[1]
                length = list(buffer[2:2 + max_length:])
                char_num = sum(length)  # 求层数
                # 如果length全零，那么表示256个字符全在同一层
                if char_num == 0 and max_length != 0:
                    char_num = 256
                    length[max_length - 1] = 256
                # 计算出还原huffman码表所需的信息
                char_lst, length_lst = [], []
                for pos in range(2 + max_length, 2 + max_length + char_num):
                    char_lst.append(int2bytes(buffer[pos]))
                for i in range(max_length):
                    length_lst.extend([i + 1] * length[i])
                code_dic = huffman.rebuilt(char_lst, length_lst)
                str_bytes = buffer[2 + max_length + char_num:]
                write_buffer = huffman.decode(str_bytes, code_dic, padding)
                fp_out.write(write_buffer)
