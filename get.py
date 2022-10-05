import os,requests
import logging
logging.basicConfig(filename="get.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
def get_mp3(name:"str"):
    try:
        url = "https://hanyu-word-pinyin-short.cdn.bcebos.com/"+name+".mp3"
        res = requests.get(url)
        if res.status_code != 200:
            logging.error("Cannot get file :{webside}, status code:{code}".format(webside = url,code=res.status_code))
        else:
            logging.info("Get file : {webside} , with status code 200".format(webside= url))
    except Exception as e:
        logging.exception(e)
