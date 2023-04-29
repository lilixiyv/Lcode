from math import log2

from Huffman import int2bytes


class lz78_decode:
    @classmethod
    def decode(cls,source_path,target_path):
        bts=open(source_path,"rb").read()
        f_out=open(target_path,"wb")
        LZ_dic={}
        myfile=bts[:3]
        bts=bts[3:]
        l_bts=len(bts)
        if myfile!=b'bdm':
            print("this is not my file")
            return None
        i=0
        while i<l_bts:
            print(LZ_dic)
            l_dic=len(LZ_dic)
            if l_dic==0:
                l_num=1
            else:
                l_num=int(log2(l_dic)/8)+1
            index=int.from_bytes(bts[i:i+l_num],'big')
            print(i+l_num,l_bts)
            if(i+l_num==l_bts):
                lastchar=b''
            else:
                lastchar=int2bytes(bts[i+l_num])
            i+=(l_num+1)
            if index ==0:
                LZ_dic[l_dic+1]=lastchar
                f_out.write(lastchar)
            else:
                before=LZ_dic[index]
                bs=before+lastchar
                LZ_dic[l_dic+1]=bs
                f_out.write(bs)


if __name__ == '__main__':
    lz78_decode.decode('./test/output.txt','./test/re.txt')