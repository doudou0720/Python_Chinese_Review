import json
import os
import datetime
import logging
import sys
import flask
import importlib
from . import utils 

__is_init__ = False
extension_logger = logging.getLogger('EXT(extensions_loader)')
extension_logger.setLevel(logging.INFO)
fh = logging.FileHandler
ch = logging.StreamHandler
run_dir = os.path.split(__file__)[0]
import_ext = {}
ext_list = []
app = flask.Flask


def init(f:logging.FileHandler,c:logging.StreamHandler,fl:flask.Flask):
    global __is_init__ , extension_logger ,app ,fh , ch
    extension_logger.addHandler(c)
    extension_logger.addHandler(f)
    fh = f
    ch = c
    app = fl
    sys.path.append(os.path.abspath(os.path.split(__file__)[0]+"/../"))
    __is_init__ = True

def ext_checker():
    global import_ext , app ,fh , ch
    if __is_init__ == False:
        raise TypeError("你尚未初始化!")
    with open("{path}/data/installed_packges.json".format(path=run_dir),'r',encoding='utf8') as f:
        json_data = json.load(f)
        past_time = datetime.datetime.now() - datetime.datetime.strptime(json_data['last_check_date'],'%Y-%m-%d')
    with open("{path}/data/installed_packges.json".format(path=run_dir),'w',encoding='utf8') as f:
        if past_time.days >= 7:
            extension_logger.info("距离上一次检查更新过去了{n}天,即将开始本次检查...".format(n=past_time.days))
            ##TODO##
            extension_logger.info("检查成功")
            json_data['last_check_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            f.write(json.dumps(json_data))
            extension_logger.info("写入json成功")
        else:
            f.write(json.dumps(json_data))
            extension_logger.info("距离上次更新时间间隔较短,暂不检查\n若想立即检查,请至设置中计划下次更新")
    length = len(json_data['data'])
    for i in range(length):
        extension_logger.info("正在导入第{n}个({name}),共{m}个".format(n = i+1,m = length,name=json_data["data"][i]["packge_name"]))
        import_ext[json_data["data"][i]["packge_name"]] = importlib.import_module(json_data["data"][i]["init_name"])
        ext_list.append(json_data["data"][i]["packge_name"])
        try:
            import_ext[json_data["data"][i]["packge_name"]].init(utils.ToExts(app,fh,ch))
        except AttributeError:
            extension_logger.warning("模块 {ext}  未定义init方法".format(ext=json_data["data"][i]["packge_name"]))
        extension_logger.info("导入完成！")

def get_ext_info(name:list = None):
    ret = []
    if name == None:
        name = ext_list
    for i in name:
        with open(import_ext[i].info_path,"r",encoding='utf8') as f:
            ret.append(json.load(f))
    return ret