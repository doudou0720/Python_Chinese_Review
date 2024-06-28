import logging
import progressbar
from flask import Flask,render_template,request,url_for,redirect
import requests
from . import stardict as sd
import os

extension_logger = logging.Logger
run_dir = ""
json_info = {}
# from run import app
app = Flask
import urllib.request

def download_files(url,name):
    response = requests.request("GET", url, stream=True, data=None, headers=None)

    save_path = "./extensions/main/english/"+name

    total_length = int(response.headers.get("Content-Length"))
    with open(save_path, 'wb') as f:
        widgets = ['Progress: ', progressbar.Percentage(), ' ',
            progressbar.Bar(marker='#', left='[', right=']'),
            ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
        for chunk in response.iter_content(chunk_size=1):
            if chunk:
                f.write(chunk)
                f.flush()
            pbar.update(len(chunk) + 1)
        pbar.finish()

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
            if cnt > 1:
                if cnt < 4:
                    try :
                        extension_logger.info("Try to download it from https://github.moeyy.xyz/ ...")
                        download_files("https://github.moeyy.xyz/https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip","ecdict-sqlite-28.zip")
                    except Exception as e:
                        extension_logger.error("The following error occurred on the {k}th download attempt(Use moeyy):\n{e}".format(k=cnt+1,e=e))
                else :
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