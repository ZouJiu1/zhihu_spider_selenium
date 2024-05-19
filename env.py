import os
import shutil
abspath = os.path.abspath(__file__)
filename = abspath.split(os.sep)[-1]
abspath = abspath.replace(filename, "")

def to_setting():
    userhome = os.path.expanduser("~")
    shutil.copyfile(os.path.join(abspath, "msedgedriver", ".condarc"), \
        userhome)
    os.system("")
    os.system("conda clean -i; Y;")
    os.system("cd %s; pip install -r requirement.txt"%(abspath, ))

def clean():
    inpath = r'C:\Users\10696\Desktop\crawler_spider\zhihu_spider_selenium\article\article.txt'
    articledir = r'C:\Users\10696\Desktop\crawler_spider\zhihu_spider_selenium\article'
    with open(inpath, 'r', encoding='utf-8') as obj:
        for i in obj.readlines():
            title = i.strip().split(" ")[-1]
            nam = title.replace(":", "_").replace("?", "_问号_"). \
                        replace("/","_").replace("\\","_").replace("\"", "_").\
                        replace("*","_").replace("|", "_").replace("？", "_问号_").replace("！", "").\
                        replace("<", "小于").replace(">", "大于").replace("(", "").\
                        replace(")", "")
            dic = {}
            for j in os.listdir(articledir):
                if nam in j and os.path.isdir(os.path.join(articledir, j)):
                    direxit = True
                    dircol = os.path.join(articledir, j)
                    for k in os.listdir(dircol):
                        if '.pdf' in k:
                            try:
                                if os.path.getsize(os.path.join(dircol, k)) > 0:
                                    if nam not in dic.keys():
                                        dic[nam] = [[os.path.getmtime(dircol), j]]
                                    else:
                                        dic[nam].append([os.path.getmtime(dircol), j])
                            except:
                                if nam not in dic.keys():
                                    dic[nam] = [[os.path.getmtime(dircol), j]]
                                else:
                                    dic[nam].append([os.path.getmtime(dircol), j])
            for key, value in dic.items():
                value = sorted(value.__iter__(), key=lambda k:k[0])
                for ij in value[:-1]:
                    for ijk in os.listdir(os.path.join(articledir, ij[-1])):
                        os.remove(str(os.path.join(articledir, ij[-1], ijk)))
                    shutil.rmtree(os.path.join(articledir, ij[-1]))

if __name__=="__main__":
    # to_setting()
    clean()