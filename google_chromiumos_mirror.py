from glob import glob
from os import chdir

from tasinghua_aosp_mirror import get_std_path, get_xml
def check_repo(args: str):
    args = get_std_path(args)
    list1 = []
    for a03 in get_tree_path(args):
        if "branch-mode" not in a03 and "xml" not in a03:
            try:
                chdir(a03)
            except:
                list1.append(a03)
    if len(list1) > 0:
        file = open("C:/error.txt", "w+")
        for i in list1: file.write(i+"\n")
        file.close()
        print("check-repo-error")
        return 1
    else:
        print("检查完毕，未发现仓库丢失。")
        return 0

def get_tree_path(arg: str):
    list1 = []
    arg = get_std_path(arg)
    xml = get_xml(arg)
    file = open(xml, "r+")
    read = file.read().split("\n")
    for i in read:
        if "name" in i and "Rename" not in i:
            i1 = i.split('"')
            i2 = i1[1]
            i2 = i2.split("<")[0]
            list1.append(arg+i2+".git")
    return list1
def check_pack(args: str,http_proxy: str = None,
                         https_proxy: str = None,):
    cmd = ""
    if http_proxy is not None:
        cmd += f"set http_proxy=http://{http_proxy}\n"
    if https_proxy is not None:
        cmd += f"set https_proxy=http://{https_proxy}\n"

    error_list = []
    none_list = []
    if 0:
        print("check-repo error")
        return 1
    else:
        args = get_std_path(args)
        tree = get_tree_path(args)
        for i in tree:
            i = i + "/objects/pack/*"
            file_list = glob(i)
            if len(file_list) % 3 != 0 and len(file_list) != 0:
                error_list.append((i, len(file_list)))
            if len(file_list) == 0:
                i = i.replace("objects/pack/*", "")
                none_list.append(i)
                i = i.replace("/", "\\")
                cmd += f"cd /d{i}\n"
                cmd += "git fetch\n"
                cmd += "TIMEOUT /T 2 /NOBREAK\n"
    if len(error_list) == 0:
        file = open("C:/runnone.bat", "w+")
        file.write(cmd)
        file.close()
        for i in none_list: print(i)
        return 0
    else:
        print(error_list)
        return 1
check_repo("H:\\chromium.googlesource.com\\chromiumos")