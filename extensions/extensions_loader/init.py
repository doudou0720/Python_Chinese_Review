import json
import os
import datetime
import logging
import sys
import flask
import importlib

__is_init__ = False
extension_logger = logging.getLogger('EXT(extensions_loader)')
extension_logger.setLevel(logging.INFO)

def init(fh:logging.FileHandler,ch:logging.StreamHandler,f:flask.Flask):
    global __is_init__ , extension_logger
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    extension_logger.addHandler(fh)
    extension_logger.addHandler(ch)
    sys.path.append(os.getcwd()+"/../../")
    __is_init__ = True

def ext_checker():
    if __is_init__ == False:
        raise TypeError("你尚未初始化!")
    with open(r"./data/installed_packges.json",'r',encoding='utf8') as f:
        json_data = json.load(f)
        past_time = datetime.datetime.now() - datetime.datetime.strptime(json_data['last_check_date'],'%Y-%m-%d')
        if past_time.days >= 7:
            extension_logger.info("距离上一次检查更新过去了{n}天,即将开始本次检查...".format(n=past_time.days))
            ##TODO##
            extension_logger.info("检查成功")
            json_data['last_check_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            extension_logger.info("写入json成功")
        length = len(json_data['data'])
        for i in range(length):
            extension_logger.info("正在导入第{n}个({name}),共{m}个".format(n = i+1,m = length,name=json_data["data"][i]["packge_name"]))
            importlib.import_module("extensions."+json_data["data"][i]["packge_name"],json_data["data"][i]["packge_name"])
        raise RuntimeError