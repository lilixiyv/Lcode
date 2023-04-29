from Huffman import huffman, int2bytes


class Encode:
    @classmethod
    def encode_as_huffman(cls, bts):
        fre_dic = huffman.fre_count(bts)
        code_dic=huffman.tree_build(fre_dic)
        code_dic = huffman.stand_huff(code_dic)
        max_length = 0
        for code in code_dic.values():
            max_length = max(max_length, len(code))
        length_lst = [0 for _ in range(max_length + 1)]
        for code in code_dic.values():
            length_lst[len(code)] += 1
        # 要是256个字符全部位于同一层，使用全零标记
        if length_lst[max_length] == 256:
            length_lst[max_length] = 0
        length_lst.pop(0)  # 码长为0的字符并不存在，故删去
        code_bytes = b''.join(code_dic.keys())
        length_bytes = b''.join(map(int2bytes, length_lst))
        temp_buffer, padding = huffman.encode(bts, code_dic)
        code_data = int2bytes(max_length) + length_bytes + code_bytes
        write_buffer = int2bytes(padding) + code_data + temp_buffer#将padding置于开头，方便处理
        return write_buffer

    @classmethod
    def encode(cls, source_path, target_path):
        with open(source_path, 'rb') as fp_in:
            with open(target_path, 'wb') as fp_out:
                write_buffer = b'bdm'+cls.encode_as_huffman(fp_in.read())
                fp_out.write(write_buffer)
        return target_path
