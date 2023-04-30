class HNode:
    def __init__(self, value, weight, l_child, r_child):
        self.value = value
        self.weight = weight
        self.l_child = l_child
        self.r_child = r_child


class Huffman:
    """
    build a huffman tree, realize the encoding and decoding of huffman;
    when encoding, need str; call the function "encode" ;
    when decoding, need str, code tree, padding; call the function "decode".
    """

    def __init__(self, str_file, huff_dic=None):
        """
        build the parameter needed in Huffman code
        :param str_file: bytes; the data to deal with;
        :param huff_dic: dictionary; needed when decoding, the stand huffman dictionary
        """
        self.str_file = str_file
        self.huff_dic = huff_dic
        self.fre_dic = {}

    @classmethod
    def huff_dic_buffer(cls, huff_dic):
        """
        build the code_data to convert the information about huffman code
        :param huff_dic: dictionary; the stand huffman dictionary that has been built
        :return: code_data: bytes;
        """
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
        return code_data

    @classmethod
    def rebuild(cls, v_lst, l_lst) -> dict:
        """
        rebuild the stand huffman dic
        :param v_lst: the list of char
        :param l_lst: the list of code length
        :return: re_huff_dic: the huffman tree
        """
        re_huff_dic = {value: '' for value in v_lst}
        re_huff_dic[v_lst[0]] = bin(0)[2:].rjust(l_lst[0], '0')
        pre = 0
        for i in range(1, len(v_lst)):
            pre = (pre + 1) << (l_lst[i] - l_lst[i - 1])
            re_huff_dic[v_lst[i]] = bin(pre)[2:].rjust(l_lst[i], '0')
        return re_huff_dic

    def _fre_count(self):
        """
        count the frequency of characters in the file;
        use the str_file and build the file_dic
        """
        cha_fre = [0 for _ in range(256)]
        for item in self.str_file:
            cha_fre[item] += 1
        for i in range(256):
            if cha_fre[i] != 0:
                self.fre_dic[bytes([i])] = cha_fre[i]

    def _tree_build(self):
        """
        build huffman tree with file_dic
        """

        def rec_code(pre, code):
            """
            code recursively
            :param pre:  pre HNode
            :param code: cur_code
            """
            if pre is None:
                return
            else:
                if pre.l_child is None and pre.r_child is None:
                    self.huff_dic[pre.value] = code
                else:
                    rec_code(pre.l_child, code + '0')
                    rec_code(pre.r_child, code + '1')

        self._fre_count()
        if not self.fre_dic:  # 没有字符
            return
        elif len(self.fre_dic) == 1:  # 仅有一个字符
            for value in self.fre_dic.keys():
                self.huff_dic[value] = '0'
            return
        h_lst = [HNode(value, weight, None, None) for value, weight in self.fre_dic.items()]
        h_lst.sort(key=lambda x: x.weight, reverse=True)

        len_h_lst = len(h_lst)
        while len_h_lst > 1:
            node2 = h_lst.pop()
            node1 = h_lst.pop()

            len_h_lst -= 2
            tmp = HNode(None, node1.weight + node2.weight, node1, node2)
            if len_h_lst == 0:
                h_lst.append(tmp)
            else:
                index = len_h_lst - 1
                while index and h_lst[index - 1].weight <= tmp.weight:
                    index -= 1
                h_lst.insert(index, tmp)
                len_h_lst += 1

        self.huff_dic = {key: '' for key in self.fre_dic}
        rec_code(h_lst[0], '')

    def stand_huff(self):
        """
        build stand Huffman re_huff_dic with huff_dic
        """
        v_lst, l_lst = [], []
        lst = [(value, len(code)) for value, code in self.huff_dic.items()]
        lst.sort(key=lambda x: (x[1], x[0]), reverse=False)
        for value, length in lst:
            v_lst.append(value)
            l_lst.append(length)
        self.huff_dic = {value: '' for value in v_lst}
        pre = 0
        self.huff_dic[v_lst[0]] = bin(pre)[2:].rjust(l_lst[0], '0')
        for i in range(1, len(v_lst)):
            pre = (pre + 1) << (l_lst[i] - l_lst[i - 1])
            self.huff_dic[v_lst[i]] = bin(pre)[2:].rjust(l_lst[i], '0')

    def encode(self):
        """
        encode: one of the main function of Huffman; use one '1' and several '0' to padding;
        :return: the data of the result of decompression and the huffman dictionary
        """
        self._tree_build()
        self.stand_huff()

        bin_buffer = ''
        write_buffer = bytearray([])
        for item in self.str_file:
            bin_buffer = bin_buffer + self.huff_dic[bytes([item])]
            while len(bin_buffer) >= 8:
                write_buffer.append(int(bin_buffer[:8], 2))
                bin_buffer = bin_buffer[8:]
        # 在最后一个字节使用一个1和若干0填充,若最后正好无多余，则要填充一个字节
        bin_buffer += '1'
        bin_buffer = bin_buffer.ljust(8, '0')
        write_buffer.append(int(bin_buffer, 2))

        return bytes(write_buffer), self.huff_dic

    def decode(self):
        if not self.huff_dic:  # 空字典
            return b''
        elif len(self.huff_dic) == 1:  # 字典长度为1，为了保证鲁棒性添加冗余
            self.huff_dic[b'lxy'] = 'lxy'
        node_lst = [HNode(value, weight, None, None) for value, weight in self.huff_dic.items()]  # value 为字符值， weight 为编码
        node_lst.sort(key=lambda x: (len(x.weight), x.weight), reverse=False)
        # 根据信息恢复码树
        while len(node_lst) > 1:
            node2 = node_lst.pop()
            node1 = node_lst.pop()
            node_add = HNode(None, node1.weight[:-1:], node1, node2)
            node_lst.append(node_add)
            node_lst.sort(key=lambda x: (len(x.weight), x.weight), reverse=False)
        read_buffer, buffer_size = [], 0
        dic = [list(map(int, bin(i)[2:].rjust(8, '0'))) for i in range(256)]  # 这只是一个对应二进制字符串的字典
        for i in self.str_file:
            read_buffer.extend(dic[i])
            buffer_size = buffer_size + 8
        padding_len = 1
        for i in read_buffer[::-1]:
            if i != 1:
                padding_len += 1
            else:
                break
        read_buffer = read_buffer[0: buffer_size - padding_len]
        buffer_size = buffer_size - padding_len
        write_buffer = bytearray([])
        current = node_lst[0]
        for pos in range(0, buffer_size, 8):
            for item in read_buffer[pos:pos + 8]:
                if item:
                    current = current.r_child
                else:
                    current = current.l_child
                # 到达叶结点，打印字符并重置current
                if current.l_child is None and current.r_child is None:
                    write_buffer.extend(current.value)
                    current = node_lst[0]

        return bytes(write_buffer)
