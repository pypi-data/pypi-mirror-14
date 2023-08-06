import os

filelist = []
dirlist = []
dirfilelist = []


def show_all(path='.', level=0):   #递归打印指定目录下所有的文件和文件
    filesordirs = os.listdir(path) #获得path目录下的所有文件和目录（非递归）
    if(filesordirs==[]):           #如果目录为空
        print(level*4*' '+'...')
    for f in filesordirs:
        dirfilelist.append(f)
        if (os.path.isdir(path + '/' + f)):
            print(level * 4*' '+ f)
            dirlist.append(path + '/' + f)
            show_all(path + '/' + f, level + 1)
        else:
            print(level * 4*' ' + f)
            filelist.append(path + '/' + f)


if __name__ == '__main__':
    show_all()
    print(dirfilelist) #递归打印指定目录下所有的文件和文件(在列表中）
