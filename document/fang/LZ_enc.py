from math import log2

from Huffman import int2bytes

"""
字典以<char,index>方式储存便于查找
"""
class lz78_encode:
    @staticmethod
    def max_find(bts,dic):
        i=1
        for key in dic:
            if bts==key:
                return i
            i+=1
        return -1


    @classmethod
    def encode(cls,source_path,target_path):
        bts=open(source_path,"rb").read()
        f_out=open(target_path,"wb")
        l_bts=len(bts)
        i=0
        LZ_dic={}
        while i<l_bts:
            print(LZ_dic)
            l_dic=len(LZ_dic)
            if l_dic==0:
                LZ_dic[int2bytes(bts[i])]=0
                f_out.write(b'bdm')#标记自己的文档
                f_out.write((0).to_bytes(1,byteorder='big'))
                f_out.write(int2bytes(bts[i]))
                i+=1
            else:
                l_num=int(log2(l_dic)/8)+1
                end=0#需要标记是否已经处理完
                pre=int2bytes(bts[i])
                value=cls.max_find(pre,LZ_dic)#预处理避免出错
                tmp=value
                while value!=-1:
                    i+=1
                    if i == l_bts:
                        end = 1
                        break
                    tmp=value
                    pre+=int2bytes(bts[i])
                    value=cls.max_find(pre,LZ_dic)
                if end==1:
                    f_out.write(value.to_bytes(l_num,'big'))
                else:
                    i+=1
                    if tmp==-1:
                        LZ_dic[pre] = 0
                        f_out.write((0).to_bytes(l_num, 'big'))
                        f_out.write(int2bytes(pre[-1]))
                    else:
                        LZ_dic[pre] = l_dic+1
                        f_out.write(tmp.to_bytes(l_num, 'big'))
                        f_out.write(int2bytes(pre[-1]))



if __name__ == '__main__':
    lz78_encode.encode('./test/input.txt','./test/output.txt')
