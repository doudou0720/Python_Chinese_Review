import shutil
import subprocess
import requests
import os,time
import json
import sys
import tempfile
import retrying
import multiprocessing
import ctypes
# import alive_progress
def copyFile(sourcePath, savePath):
    items = os.listdir(sourcePath)
    for item in items:
        filePath = os.path.join(sourcePath, item)
        if os.path.isfile(filePath):
            shutil.copyfile(filePath, os.path.join(savePath,item)) # 复制文件到目标文件夹
            print(' 复制成功 ' + filePath+"\r",end="")
        elif os.path.isdir(filePath):
            os.makedirs(os.path.join(savePath,item),exist_ok=True)
            copyFile(filePath, os.path.join(savePath,item)) # 如果是文件夹，则再次调用此函数，递归处理

def popen(s):
    global cnt
    print(">",s)
    s = os.popen(s)
    print(s.read())
    cnt.value+=1
    print("Finish",cnt.value,"Tasks")
def clean(sep=0):
    time.sleep(sep)
    if sys.platform.startswith("win"):
        os.system("cls")
    elif sys.platform.startswith("linux"):
        os.system("clear")
    elif sys.platform.startswith("darwin"):
        os.system("clear")
    else:
        print("当前系统是其他操作系统(识别为:{name}),暂不支持\r".format(name=str(sys.platform)),end="")
    
if __name__ == "__main__":
    print("""
    ######################
    #     PCR 引导程序    #
    ######################

    Ver. 1.0
    """)
    clean(1)

    if os.path.exists("./start.json"):
        pass
    else:
        cnt = multiprocessing.Manager().Value(ctypes.c_int,0)
        print("项目初始化中...")
        clean(0.5)
        print("在使用本软件前,请先阅读本软件所使用的所有软件的开源许可证:\nBootstrap & Bootstrap Icons & jQuery: MIT License\nLXGW : SIL OPEN FONT LICENSE Version 1.1\n其余未列出项目将于开发结束后列出")
        if bool(input("Do you want to download Git?\nThis is necessary , if you want to start later,input Nothing.\n输入任意内容回车以下载MinGit,若没有输入,程序则会自动退出\n>>")) == False:
            exit(0)
        os.makedirs("./bin/MinGit",exist_ok=True)
        if sys.platform.startswith("win"):
            print("请打开 https://mirrors.tuna.tsinghua.edu.cn/github-release/git-for-windows/git/LatestRelease 下载MinGit-<版本号>-<32-bit>/<64-bit>/<arm64>.zip,将压缩包下内容放入./bin/MinGit下")
            print("程序会自动检测进入下一环节...\r",end="")
            while True:
                if os.path.exists("./bin/MinGit/cmd/git.exe"):
                    print("程序已检测到git.exe,进入下一环节...")
                    time.sleep(2)
                    break

                time.sleep(1)        
        elif sys.platform.startswith("linux"):
            print("请打开命令行，输入:\n> sudo apt update\n> sudo apt upgrade\n> sudo apt install git\n> sudo ln -s ./bin/MinGit <你的Git可执行文件位置>")
            input("然后按下回车\n>>")
        else:
            print("当前系统是其他操作系统(识别为:{name}),暂不支持\r".format(name=str(sys.platform)),end="")

        with tempfile.TemporaryDirectory() as dir:
            clean()
            print("STEP(1) 克隆元数据")
            cnt.value=0
            @retrying.retry()
            def CloneMeta():
                global dir
                time.sleep(5)
                p = multiprocessing.Pool(processes=5)
                if sys.platform.startswith("win"):    
                    p.apply_async(popen,(f"\"{os.path.join(os.path.split(__file__)[0],'./bin/MinGit/cmd/git.exe')}\" clone --filter=blob:none --sparse https://gitee.com/mirrors/bootstrap.git "+str(dir)+"/BootStrap" ,))
                    p.apply_async(popen,(f"\"{os.path.join(os.path.split(__file__)[0],'./bin/MinGit/cmd/git.exe')}\" clone --filter=blob:none --sparse https://gitclone.com/github.com/lxgw/LxgwWenKai.git "+str(dir)+"/Lxgw" ,))
                    p.apply_async(popen,(f"\"{os.path.join(os.path.split(__file__)[0],'./bin/MinGit/cmd/git.exe')}\" clone -b 3.7.1 --filter=blob:none --sparse https://gitee.com/mirrors/jQuery.git "+str(dir)+"/jQuery" ,))
                    p.apply_async(popen,(f"\"{os.path.join(os.path.split(__file__)[0],'./bin/MinGit/cmd/git.exe')}\" clone --filter=blob:none --sparse https://gitee.com/mirrors/Bootstrap-Icons.git "+str(dir)+"/BootStrapIcons" ,))
                elif sys.platform.startswith("linux"):
                    p.apply_async(popen,(f"git clone --filter=blob:none --sparse https://gitee.com/mirrors/bootstrap.git "+str(dir)+"/BootStrap" ,))
                    p.apply_async(popen,(f"git clone --filter=blob:none --sparse https://gitclone.com/github.com/lxgw/LxgwWenKai.git "+str(dir)+"/Lxgw" ,))
                    p.apply_async(popen,(f"git clone -b 3.7.1 --filter=blob:none --sparse https://gitee.com/mirrors/jQuery.git "+str(dir)+"/jQuery" ,))
                    p.apply_async(popen,(f"git clone --filter=blob:none --sparse https://gitee.com/mirrors/Bootstrap-Icons.git "+str(dir)+"/BootStrapIcons" ,))
                p.close()
                p.join()
                if os.listdir(str(dir)+"/BootStrapIcons") != [] and os.listdir(str(dir)+"/BootStrap") != [] and os.listdir(str(dir)+"/Lxgw") != [] and os.listdir(str(dir)+"/jQuery") != []:
                    return
                else:
                    raise ConnectionError("Clone Error!")
            CloneMeta()
            del CloneMeta
            clean(0.5)
            print("STEP(2) 克隆数据")
            cnt.value = 0
            @retrying.retry()
            def CloneMeta():
                global dir
                p = multiprocessing.Pool(processes=5)
                if sys.platform.startswith("win"):
                    command = f"\"{os.path.abspath(os.path.join(os.path.split(__file__)[0],'./bin/MinGit/cmd/git.exe'))}\" "
                    p.apply_async(popen,(f"cd /D {dir}/Bootstrap && {command} sparse-checkout add dist" ,))
                    p.apply_async(popen,(f"cd /D {dir}/Lxgw && {command} sparse-checkout add fonts/TTF" ,))
                    p.apply_async(popen,(f"cd /D {dir}/jQuery && {command} sparse-checkout add dist" ,))
                    p.apply_async(popen,(f"cd /D {dir}/BootStrapIcons && {command} sparse-checkout add icons && {command} sparse-checkout add font" ,))
                elif sys.platform.startswith("linux"):
                    command = "git"
                    p.apply_async(popen,(f"cd {dir}/Bootstrap;{command} sparse-checkout add dist" ,))
                    p.apply_async(popen,(f"cd {dir}/Lxgw;{command} sparse-checkout add fonts" ,))
                    p.apply_async(popen,(f"cd {dir}/jQuery;{command} sparse-checkout add dist" ,))
                    p.apply_async(popen,(f"cd {dir}/BootStrapIcons;{command} sparse-checkout add icons" ,))
                p.close()
                p.join()
                if os.listdir(str(dir)+"/BootStrapIcons") != [] and os.listdir(str(dir)+"/BootStrap") != [] and os.listdir(str(dir)+"/Lxgw") != [] and os.listdir(str(dir)+"/jQuery") != []:
                    return
                else:
                    raise ConnectionError("Clone Error!")
            CloneMeta()
            clean(0.5)
            print("STEP(3) Copy")
            os.makedirs("./static/js",exist_ok=True)
            os.makedirs("./static/css",exist_ok=True)
            os.makedirs("./static/fonts",exist_ok=True)
            os.makedirs("./static/icons",exist_ok=True)
            shutil.move(os.path.join(dir,"./jQuery/dist/jquery.js"),"./static/js/jquery-3.6.1.js")  #Although it is not 3.6.1 :)
            copyFile(os.path.join(dir,"./BootStrap/dist/css/"),"./static/css")
            copyFile(os.path.join(dir,"./BootStrap/dist/js/"),"./static/js")
            copyFile(os.path.join(dir,"./BootStrapIcons/icons/"),"./static/icons")
            copyFile(os.path.join(dir,"./Lxgw/fonts/TTF/"),"./static/fonts")
            copyFile(os.path.join(dir,"./BootStrapIcons/font/"),"./static/css")
