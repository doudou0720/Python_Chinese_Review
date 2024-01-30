import os
import flask
from . import main
import logging

extension_logger = logging.getLogger('EXT(main.basic.english.reading)')
extension_logger.setLevel(logging.INFO)
run_dir = os.path.split(__file__)[0]
info_path = run_dir+"/init.json"

def init(k:flask.Flask,fh:logging.FileHandler,ch:logging.StreamHandler):
    global run_dir
    extension_logger.addHandler(ch)
    extension_logger.addHandler(fh)
    if not os.path.exists(info_path):
        extension_logger.error("未找到JSON文件，该拓展将不会被加载!")
        return
    main.init(k,extension_logger,run_dir)