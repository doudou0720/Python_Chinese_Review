import logging
import time 
from flask import Flask,render_template,request,url_for,redirect,abort,Response
import requests
try:
    import stardict
except:
    from . import stardict
import os
import hashlib
import zipfile

extension_logger = logging.Logger
run_dir = ""
json_info = {}
# from run import app
app = Flask
def download_files(url,name):
    global extension_logger
    filepath = "./extensions/main/english/"+name
    # if not os.path.exists(path):   # 看是否有该文件夹，没有则创建文件夹
    #     os.mkdir(path)
    start = time.time() #下载开始时间
    response = requests.get(url, stream=True) #stream=True必须写上
    size = 0    #初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:   #判断是否响应成功
            st = time.time()
            extension_logger.info('[Download Progress] Start download,[File size]:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   #开始下载，显示下载文件大小
            with open(filepath,'wb') as file:   #显示进度条
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+'[Download Progress] (Total  ' + str(content_size) + ' Bytes , Now  ' + str(size) + ' Bytes ) :%.2f%%' % (float(size / content_size * 100)) ,end=' ')
            ft = time.time()
            print("\r[Download Progress] (Total  {k} Bytes) 100.00% Finish in {s}s                ".format(k=content_size,s=ft-st))
        else:
            extension_logger.error("[Download Progress] HTTP Status Code {code}".format(code=response.status_code))
        end = time.time()   #下载结束时间
        extension_logger.info('Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
    except Exception as e:
        extension_logger.exception(e)

def check_md5(path,md5):
    global extension_logger
    with open(path,"rb") as f:
        file_md5 = hashlib.md5(f.read()).hexdigest()
    if file_md5 != md5:
        extension_logger.error("MD5 Dismatch!({n} do not match {c})".format(n=file_md5,c=md5))
        extension_logger.error("The dictionary part WILL NOT be loaded")
        return False
    return True

def deal_single_word(word_c):
    word_c = str(word_c)
    word = ""
    for i in range(len(word_c)):
        if word_c[i].lower() in "abcdefghijklmnopqrstuvwxyz'-":
            word += word_c[i].lower()
    return word

cl = r'./extensions/main/english/stardict.db'
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
        if input("\nAre you in countries that CANNOT visit Github?\n你是否能流畅访问 github.com ?\n如果不能,请按y并回车\nIf you can , just press the 'Enter' button.\n>>") == "y":
            url = "https://github.moeyy.xyz/https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"
        else:
            url = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"
        while True:
            if cnt > 2:
                extension_logger.error("Cannot Download Files!The dictionary part WILL NOT be loaded")
                return
            try:
                extension_logger.info("Download 'ecdict-sqlite-28.zip' from "+url)
                download_files(url,"ecdict-sqlite-28.zip")
                break
            except Exception as e:
                extension_logger.error("The following error occurred on the {k}th download attempt:\n{e}".format(k=cnt+1,e=e))
                cnt += 1
                continue
        #zip md5校验
        if check_md5("./extensions/main/english/ecdict-sqlite-28.zip",'9bbd6a5364a1f20ca35e32870569ef8b') == False:
            return
        extension_logger.info("解压zip文件...")
        (zipfile.ZipFile("./extensions/main/english/ecdict-sqlite-28.zip")).extractall("./extensions/main/english/")
        if check_md5("./extensions/main/english/stardict.db",'4e360fc0d9ecf602069d0cead54664c6') == False:
            return
        os.remove("./extensions/main/english/ecdict-sqlite-28.zip")
        
        
    @app.route("/extension/main.basic.english.dictionary/")
    def home():
        return render_template("extensions/main/english/dictionary/Scratch.html")
    @app.route("/extension/main.basic.english.dictionary/s/<word>/")
    def seratch(word):
        global cl,extension_logger
        word = deal_single_word(word)
        ru = stardict.StarDict(cl,True).match(word,strip=True)
        other = stardict.StarDict(cl,True).query(word)
        ru2 = []
        if other == None:
            print(word)
            return "未能查询相关信息，这通常意味着这个词为政治新词，请到<a href='https://www.deepl.com/zh/translator#en/zh/"+ word +"' target='_blank'>DeepL</a>查询"
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
        try:
            is_simple = request.args.get("is_simple")
            if is_simple.lower() == "true":
                is_simple = True
            elif is_simple.lower() == "false":
                is_simple = False
            else:
                extension_logger.error("Invalid input on value 'is_simple': "+is_simple)
                extension_logger.warning("Set 'is_simple' to False")
                is_simple = False
        except Exception as e:
            extension_logger.warning("CANNOT get 'is_simple' , See the error below:\n"+e)
            is_simple = False
        return render_template("extensions/main/english/dictionary/result.html",rl = ru2,definition = c_list_e,translation = c_list_c,word = other["word"],id = other["id"],exchange = nexchange,tag=tag,is_simple=is_simple)

    @app.route("/extension/main.basic.english.dictionary/jump/")
    def jump():
        try:
            is_simple = request.args.get("is_simple")
        except Exception as e:
            extension_logger.warning("CANNOT get 'is_simple' , See the error below:\n"+e)
            is_simple = "False"
        a = request.values.get("word")
        return redirect("/extension/main.basic.english.dictionary/s/"+str(a)+"?is_simple="+str(is_simple))
    extension_logger.info("Load main.basic.english.dictionary successfully!")

    # "get"下属于技术性网址，供其他模块使用
    @app.route("/extension/main.basic.english.dictionary/get/root")
    def get_root():
        global deal_single_word
        try:
            word = request.args.get("word")
            word = deal_single_word(word)
            other = stardict.StarDict(cl,True).query(word)
        except Exception as e:
            return Response(str(e),404)
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
        for i in nexchange:
            if i[0] == '0':
                return i[1]
        return word

if __name__ == "__main__":
    app.run(host="0.0.0.0")