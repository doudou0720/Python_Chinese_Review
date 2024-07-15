import os
import logging
from flask import Flask,render_template,request

extension_logger = logging.Logger
run_dir = os.path.split(__file__)[0]
info_path = run_dir+"/init.json"

def init(receive_obj):
    global run_dir
    extension_logger = receive_obj.create_logger("main.basic.common")
    if not os.path.exists(info_path):
        extension_logger.error("未找到JSON文件，该拓展将不会被加载!")
        return
    app = Flask()
    # app = receive_obj.app

    @app.route("/extension/main.basic.common/blank") #填空
    def blank():
        id = request.args.get("id")

        with open(f"{os.getcwd()}/data/Articles/Questions/{id}","r") as f:
            #TODO
            pass
        return render_template()