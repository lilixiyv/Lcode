from Huffman import Huffman
from LZ78 import LZ78


def huffman_encode(source_path, target_path):
    with open(source_path, 'rb') as fp_in, open(target_path, 'wb') as fp_out:
        str_file = fp_in.read()
        if not str_file:  # 若为空文件，直接返回空文件
            return
        huffman = Huffman(str_file)
        write_buffer, huff_dic = huffman.encode()
        code_data = Huffman.huff_dic_buffer(huff_dic)
        write_buffer = code_data + write_buffer
        write_buffer = b'lxy' + write_buffer
        fp_out.write(write_buffer)


def huffman_decode(source_path, target_path):
    with open(source_path, 'rb') as fp_in, open(target_path, 'wb') as fp_out:
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


def lz78_encode(source_path, target_path):
    f_in = open(source_path, "rb")
    str_file = f_in.read()
    if not str_file:
        return
    f_out = open(target_path, "wb")
    f_out.write(b'lxy')  # 标记文档
    lz78 = LZ78(source_path, target_path)
    lz78.encode()


def lz78_decode(source_path, target_path):
    str_file = open(source_path, "rb")
    if not str_file:
        return
    flag_file = str_file[:3]
    if flag_file != b'lxy':
        return -1
    lz78 = LZ78(source_path, target_path)
    lz78.decode()
