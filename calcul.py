import re
import os
import numpy as np
import shutil

def calcul():
    inpath = r'C:\Users\10696\Desktop\access\zhihu\log\2023-06-30T14_45_24.317925_log.txt'

    kk = []
    with open(inpath, 'r') as obj:
        for i in obj.readlines():
            result = re.search('\d+\.\d+', i)
            kk.append(float(result[0]))
    kk.sort()
    kk = kk[:-1]
    np.mean(kk)

def choose_noimg():
    inpath = r'C:\Users\10696\Desktop\access\zhihu\answer'
    outpath = r'C:\Users\10696\Desktop\access\zhihu\tmp'
    for i in os.listdir(inpath):
        kkk = -9
        nth = os.path.join(inpath, i)
        if os.path.isfile(nth):
            continue
        for j in os.listdir(nth):
            if '.jpg' in j:
                kkk = 9
        if kkk < 0:
            shutil.copytree(nth, os.path.join(outpath, i))

if __name__ == "__main__":
    # calcul()
    choose_noimg()