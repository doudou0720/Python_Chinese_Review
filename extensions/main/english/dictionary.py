import logging
from flask import Flask,render_template,request,url_for,redirect
from . import stardict as sd
import os

extension_logger = logging.Logger
run_dir = ""
json_info = {}
# from run import app
app = Flask
#多线程下载部分摘自https://blog.csdn.net/as604049322/article/details/119847193
import asyncio
import httpx
import requests


def calc_divisional_range(filesize, chuck=10):
    step = filesize//chuck
    arr = list(range(0, filesize, step))
    result = []
    for i in range(len(arr)-1):
        s_pos, e_pos = arr[i], arr[i+1]-1
        result.append([s_pos, e_pos])
    result[-1][-1] = filesize-1
    return result



def download_files(url,save_name):
    # 下载方法
    async def async_range_download(save_name, s_pos, e_pos):
        headers = {"Range": f"bytes={s_pos}-{e_pos}"}
        extension_logger.info("Trying to get:{url}:{}")
        res = await client.get(url, headers=headers)
        
        with open(save_name, "rb+") as f:
            f.seek(s_pos)
            f.write(res.content)
    client = httpx.AsyncClient(timeout=None)

    res = httpx.head(url)
    filesize = int(res.headers['Content-Length'])
    divisional_ranges = calc_divisional_range(filesize, 20)


    # 先创建空文件
    with open(save_name, "wb") as f:
        pass

    loop = asyncio.get_event_loop()
    tasks = [async_range_download(save_name, s_pos, e_pos)
            for s_pos, e_pos in divisional_ranges]
    # 等待所有协程执行完毕
    loop.run_until_complete(asyncio.wait(tasks))


cl = r'.\dict_l.db'
def init(k:Flask,ext_logger:logging.Logger,run_d:str):
    global app ,extension_logger ,run_dir
    app = k
    extension_logger = ext_logger
    run_dir = run_d
    if os.path.exists(cl) == False:
        extension_logger.warning("Cannot find DataBase , try to download it from https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip")
        extension_logger.info("[For countries that cannot connect to Github]If the download is too slow, you can try to download it manually by saving it under {path}/temp_dict".format(path=run_d))
        extension_logger.info("[For countries that cannot connect to Github]如果下载速度过慢，你可以尝试手动下载，保存到{path}/temp_dict下".format(path=run_d))
        cnt = 0
        while True:
            if cnt >= 5:
                extension_logger.error("Cannot Download Files!The dictionary part WILL NOT be loaded")
                return
            try:
                download_files("https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip","ecdict-sqlite-28.zip")
            except Exception as e:
                extension_logger.error("The following error occurred on the {k}th download attempt:\n{e}".format(k=cnt+1,e=e))
                cnt += 1
                continue
            break
    @app.route("/extension/main.basic.english.dictionary/")
    def home():
        return render_template("Scratch.html")
    @app.route("/extension/main.basic.english.dictionary/s/<word>/")
    def seratch(word):
        global cl
        word = str(word)
        ru = sd.StarDict(cl,True).match(word,strip=True)
        other = sd.StarDict(cl,True).query(word)
        ru2 = []
        if other == None:
            print(word)
        for i in ru:
            ru2.append(i[1])
        try:
            c_list_e = other["definition"].splitlines()
        except:
            c_list_e = ["暂无数据"]
        if c_list_e == []:
            c_list_e = ["暂无数据"]
        try:
            c_list_c = other["translation"].splitlines()
        except:
            c_list_c = ["暂无数据"]
        if c_list_c == []:
            c_list_c = ["暂无数据"]
        try:
            exchange = other["exchange"].split("/")
        except:
            exchange = []
        nexchange = []
        if exchange == []:
            nexchange = ["暂无数据"]
        else:
            for i in exchange:
                nexchange.append(i.split(":"))
        try:
            tag = other["tag"].split(" ")
        except:
            tag = []
        return render_template("result.html",rl = ru2,definition = c_list_e,translation = c_list_c,word = other["word"],id = other["id"],exchange = nexchange,tag=tag)

    @app.route("/extension/main.basic.english.dictionary/jump/")
    def jump():
        a = request.values.get("word")
        return redirect("/s/"+str(a))
    extension_logger.info("Load main.basic.english.dictionary successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0")