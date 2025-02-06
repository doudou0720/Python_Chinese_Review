import os
import logging
from flask import Flask,render_template,request

extension_logger = logging.Logger
run_dir = os.path.split(__file__)[0]

def init(receive_obj):
    global run_dir
    extension_logger = receive_obj.create_logger("main.basic.question_providers")
    #搜索提供脚本
    extension_logger.info("Searching Scripts...")
    SFile = os.listdir(os.path.join(run_dir,"./"))
    tmp = []
    for i in range(len(SFile)):
        if os.path.isfile(os.path.join(run_dir,SFile[i])):
            extension_logger.debug("File {file} Found".format(file=os.path.join(run_dir,SFile[i])))
        else:
            tmp.append(i)
    SFile.reverse()
    for i in tmp:
        SFile.remove(i)
    del tmp
    extension_logger.info("Found {k} Script(s)".format(k=len(SFile)))
    app = receive_obj.app