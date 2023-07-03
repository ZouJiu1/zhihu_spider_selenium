#################
###ZouJiu-202306
#################

import os

def dealthink(inpath):
    dic = {}
    for root, dirk, files in os.walk(inpath):
        for i in files:
            if '.txt' not in i:
                continue
            with open(os.path.join(root, i), 'r', encoding='utf-8') as obj:
                kk = obj.read()
                dic[i] = kk
    dic = sorted(dic.items(), key= lambda k:k[0])
    with open(os.path.join(inpath, 'all_txt.txt'), 'w', encoding='utf-8') as obj:
        for key, value in dic:
            obj.write(key+"\n"+value+"\n")
        
if __name__=="__main__":
    inpath = r'C:\Users\10696\Desktop\access\zhihu\think'
    dealthink(inpath)