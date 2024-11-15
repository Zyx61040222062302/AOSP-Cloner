from os import chdir, system
from glob import glob

class Path:
    def __init__(self, path: str):
        try:
            chdir(path)
        except:
            raise
        else:
            self.path = path

def get_std_path(args: str):
    if "\\" in args:
        args = args.replace("\\", "/")
    if args[-1] != "/":
        args = args + "/"
    return args
def get_xml(args: str):
    args = get_std_path(args)
    return f"{args}.repo/manifests/default.xml"
def check_repo(args: str):
    args = get_std_path(args)
    list1 = []
    for a03 in get_tree_path(args):
            try:
                chdir(a03)
            except:
                list1.append(a03)
    if len(list1) > 0:
        print(list1)
        return 1
    else:
        print("检查完毕，未发现仓库丢失。")
        return 0
def get_tree_path(args: str):
    args = get_std_path(args)
    file = open(get_xml(args), mode="r")
    read = file.read().split("\n")
    file.close()
    list1 = []
    for read_line in read:
        if "project" in read_line:
            a01 = read_line.replace('" />', "")
            a02 = a01.replace('  <project name="', "")
            a03 = a02 + '.git'
            if 'path="' in a03:
                a03 = a03.split(" path=")[0]
                a03 = a03.split('"')[0]
                a03 = a03 + ".git"
            a03 = args + a03
            list1.append(a03)
    return list1
def check_pack(args: str):
    cmd = ""
    error_list = []
    none_list = []
    if check_repo(args) != 0:
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
def tree_path_to_cmd(args: str, second: int = 2):
    cmd = ""
    list1 = get_tree_path(args)
    for i in list1:
        i = i.replace("/", "\\")
        cmd += f"cd /d{i}\n"
        cmd += "git fetch\n"
        cmd += f"TIMEOUT /T {second} /NOBREAK\n"
    file = open("c:/run.bat", "w+")
    file.write(cmd)
    file.close()
    print("写入完毕，按回车键退出。")
def fetch_128_error_repo(args: str,
                         http_proxy: str = None,
                         https_proxy: str = None,
                         second: int = 2):
    cmd = ""
    if http_proxy is not None:
        cmd += f"set http_proxy=http://{http_proxy}\n"
    if https_proxy is not None:
        cmd += f"set https_proxy=http://{https_proxy}\n"
    args = get_std_path(args)
    file = open(f"{args}error.txt", "r")
    a = file.read().split("\n")
    file.close()
    for i in a:
        i1 = i.split("'")
        i2 = i1[1]
        i3 = i1[2]
        if "exit status 128" in i3:
            i4 = args + i2
            i5 = i4.replace("/", "\\")
            cmd += f"cd /d{i5}.git\n"
            cmd += "git fetch\n"
            cmd += f"TIMEOUT /T {second} /NOBREAK\n"
    file = open("C:/run.bat", "w+")
    file.write(cmd)
    file.close()
    print("写入完成。")




