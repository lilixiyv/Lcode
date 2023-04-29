def int2bytes(n: int) ->bytes:
    return bytes([n])#将acs码值转化为bytes串


class h_node:
    def __init__(self,value,weight,lchild,rchild):
        self.value=value
        self.weight=weight
        self.lchild=lchild
        self.rchild=rchild


class huffman:
    @staticmethod
    def fre_count(bst):
        fre_dic=[0 for i in range(256)]
        for item in bst:
            fre_dic[item]+=1
        dict={}
        for i in range(256):
            if fre_dic[i]!=0:#非0才有统计必要
                dict[int2bytes(i)] = fre_dic[i]
        return dict
    @staticmethod
    def tree_build(fre_dic):
        def rec(pre,code,huff_dic):#递归编码
            if pre is None:
                return
            else:
                if pre.lchild is None and pre.rchild is None:
                    huff_dic[pre.value]=code
                else:
                    rec(pre.lchild,code+'0',huff_dic)
                    rec(pre.rchild,code+'1',huff_dic)
        if not fre_dic:#处理文档为空的情况
            return {}
        elif len(fre_dic)==1:#处理仅有一种字符的情况
            dic2={}
            for value in fre_dic.keys():
                dic2[value]='0'
            return dic2
        hlst =[h_node(value,weight,None,None)for value,weight in fre_dic.items()]
        hlst.sort(key=lambda x: x.weight,reverse=True)#降序排序，方便插入
        # 合并节点，构建树
        while(len(hlst)>1):
            node2=hlst.pop()#min
            node1=hlst.pop()#max
            tmp=h_node(None,node1.weight+node2.weight,node1,node2)
            hlst.append(tmp)
            index = len(hlst) - 1
            while index and hlst[index-1].weight<=tmp.weight:
                hlst[index]=hlst[index-1]
                index-=1
            hlst[index]=tmp
        huff_dic={key: '' for key in fre_dic}
        rec(hlst[0],'',huff_dic)
        return huff_dic

    @classmethod
    def stand_huff(cls,huffman_dic):
        #转化为范式huffman
        v_lst, l_lst = [], []
        lst=[(value,len(code)) for value,code in huffman_dic.items()]
        lst.sort(key=lambda x:(x[1],x[0]),reverse=False)#通过长度先排序，再通过asc值排序，将长且值大的放后边
        for value,lenth in lst:
            v_lst.append(value)
            l_lst.append(lenth)
        return cls.rebuilt(v_lst, l_lst)

    @staticmethod
    def rebuilt(v_lst,l_lst):
        re_huff_dic={value: ''for value in v_lst}
        pre=0
        for i in range(len(v_lst)):
            if i==0:
                pre=0
            else:
                pre=(pre+1)<<(l_lst[i]-l_lst[i-1])#核心构建思路，同一层就靠加，不同层就要左移对应位数
            re_huff_dic[v_lst[i]]=bin(pre)[2:].rjust(l_lst[i],'0')#以零来填充不满的位数
        return re_huff_dic

    @staticmethod
    def encode(bts,huffman_dic):
        bin_buffer = ''
        padding = 0
        dic = [int2bytes(i) for i in range(256)]
        read_buffer = [dic[i] for i in bts]
        #直接查找写入
        write_buffer = bytearray([])
        # 循环读入数据，同时编码输出
        for item in read_buffer:
            bin_buffer = bin_buffer + huffman_dic[item]
            while len(bin_buffer) >= 8:
                write_buffer.append(int(bin_buffer[:8], 2))
                bin_buffer = bin_buffer[8:]
        # 将缓冲区内的数据填充后输出
        if bin_buffer:
            padding = 8 - len(bin_buffer)#不够了就要补
            bin_buffer = bin_buffer.ljust(8, '0')
            write_buffer.append(int(bin_buffer, 2))

        return bytes(write_buffer), padding

    @staticmethod
    def decode(bts, huffman_dic, padding):
        if not huffman_dic:  # 空字典，直接返回
            return b''
        elif len(huffman_dic) == 1:  # 字典长度为1，为了保证鲁棒性添加冗余
            huffman_dic[b'bdm'] = 'bdm'
        node_lst = [h_node(value, weight, None, None) for value, weight in huffman_dic.items()]
        node_lst.sort(key=lambda x: (len(x.weight), x.weight), reverse=False)
        #根据信息恢复码树
        while len(node_lst) > 1:
            node2 = node_lst.pop()
            node1 = node_lst.pop()
            node_add = h_node(None, node1.weight[:-1:], node1, node2)
            node_lst.append(node_add)
            node_lst.sort(key=lambda x: (len(x.weight), x.weight), reverse=False)
        read_buffer, buffer_size = [], 0
        dic = [list(map(int, bin(i)[2:].rjust(8, '0'))) for i in range(256)]#这只是一个对应二进制字符串的字典
        for i in bts:
            read_buffer.extend(dic[i])
            buffer_size = buffer_size + 8
        read_buffer = read_buffer[0: buffer_size - padding]
        buffer_size = buffer_size - padding#得到字符串二进制长度以及二进制串
        write_buffer = bytearray([])
        current = node_lst[0]
        for pos in range(0, buffer_size, 8):
            for item in read_buffer[pos:pos + 8]:
                if item:
                    current = current.rchild
                else:
                    current = current.lchild
                # 到达叶结点，打印字符并重置current
                if current.lchild is None and current.rchild is None:
                    write_buffer.extend(current.value)
                    current = node_lst[0]


        return bytes(write_buffer)
