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

if __name__=="__main__":
    to_setting()