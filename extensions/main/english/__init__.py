import os
import flask
from . import reading,dictionary
import logging

extension_logger = logging.Logger
run_dir = os.path.split(__file__)[0]
info_path = run_dir+"/init.json"

def init(receive_obj):
    global run_dir
    extension_logger = receive_obj.create_logger("main.basic.english")
    if not os.path.exists(info_path):
        extension_logger.error("未找到JSON文件，该拓展将不会被加载!")
        return
    reading.init(receive_obj.app,receive_obj.GetSubLogger(extension_logger,"Reading"),run_dir)
    dictionary.init(receive_obj.app,receive_obj.GetSubLogger(extension_logger,"Dictionary"),run_dir)