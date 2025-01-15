"""
本模块使用目录下json对记录模块进行导入
未被记录的模块不会被导入
"""
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
    """
    加载器初始化
    """
    global __is_init__ , extension_logger ,app ,fh , ch
    #传入主程序logger
    extension_logger.addHandler(c)
    extension_logger.addHandler(f)
    fh = f
    ch = c
    #传入主程序flask App
    app = fl
    #解决相对引用
    sys.path.append(os.path.abspath(os.path.split(__file__)[0]+"/../"))
    #Flag
    __is_init__ = True

def ext_checker():
    """
    加载器主入口
    应先行执行init()
    """
    global import_ext , app ,fh , ch
    if __is_init__ == False:
        print("[WARN]你尚未初始化!,自动调用...") #检测是否初始化
        init()
        if __is_init__ == False: #二次检测
            raise("Cannot exec init()")
    with open("{path}/data/installed_packges.json".format(path=run_dir),'r',encoding='utf8') as f: #读取json,检测过期时间
        json_data = json.load(f)
        past_time = datetime.datetime.now() - datetime.datetime.strptime(json_data['last_check_date'],'%Y-%m-%d')
    #TODO:检查更新 Start
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
            extension_logger.info("距离上次更新时间间隔较短,暂不检查")
            extension_logger.info("若想立即检查,请至设置中计划下次更新")
    #TODO End
    length = len(json_data['data']) #获取总长度
    for i in range(length):
        extension_logger.info("正在导入第{n}个({name}),共{m}个".format(n = i+1,m = length,name=json_data["data"][i]["packge_name"]))
        import_ext[json_data["data"][i]["packge_name"]] = importlib.import_module(json_data["data"][i]["init_name"]) #导入库
        ext_list.append(json_data["data"][i]["packge_name"]) #存储
        try:
            import_ext[json_data["data"][i]["packge_name"]].init(utils.ToExts(app,fh,ch)) #调用init方法
        except AttributeError:
            extension_logger.error("模块 {ext}  未定义init方法".format(ext=json_data["data"][i]["packge_name"]))
        extension_logger.info("导入完成！")

def get_ext_info(name:list = None):
    """
    对run.py拓展设置提供显示
    :input name(List) 指定名称列表 
    """
    ret = []
    if name == None:#没有指定默认为空
        name = ext_list
    for i in name:
        with open(import_ext[i].info_path,"r",encoding='utf8') as f:
            ret.append(json.load(f))
    return ret