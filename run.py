import uuid
import json
from flask import Flask, make_response , render_template , request ,jsonify 
import logging
# 创建日志
main_logger=logging.getLogger('MAIN')
main_logger.setLevel(logging.INFO)
logfile = './log.log'
fh = logging.FileHandler(logfile, mode='w',encoding='utf-8')  # open的打开模式这里可以进行参考
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关
formatter = logging.Formatter("%(asctime)s - %(filename)s(%(name)s)[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
main_logger.addHandler(fh)
main_logger.addHandler(ch)
# 创建应用实例
app = Flask(__name__,template_folder="./templates",static_folder="./static")
 
# 载入拓展
main_logger.info("载入拓展...")
try:
    import extensions.extensions_loader.init as extensions_loader
    extensions_loader.init(fh,ch,app)
    extensions_loader.ext_checker()
except Exception as e:
    main_logger.exception(e)
    main_logger.critical("扩展加载存在问题!程序自动终止，请向作者进行反馈!")
    exit(-1)
# 视图函数（路由）
@app.route('/home')#主页
def index():
    """
    主页展示函数
    :input None
    :return string
    """
    return render_template("home.html",user_name = "test")

@app.route('/about')#关于
def about():
    """
    关于页展示函数
    :input None
    :return string
    """
    return render_template("about.html")

@app.route('/history')#历史
def history():
    return render_template(
        "history.html",
        historys=[
            {
                "title":"Test",
                "description":"Test,too",
                "id":114514
            },
            {
                "title":"Test2",
                "description":"Test2,too",
                "id":5201314
            }
        ]
    )

@app.route('/whiledoing')#任务进行时
def while_doing():
    return render_template("whiledoing.html")

@app.route('/settings')#设置
def settings():
    return render_template("settings.html")

@app.route('/extension')#拓展列表
def show_extensions():
    return render_template("show_extensions.html",exts=extensions_loader.get_ext_info())

@app.route('/extension/<name>')#拓展列表
def show_extensions_more(name):
    ext = (extensions_loader.get_ext_info([name])[0])
    return render_template("show_extensions_more.html",ext=ext)

logging.info("程序拓展启动完成!")
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    print("MAIN ID:",id(app))
    # app.run(debug=True,port=5000,host="0.0.0.0",ssl_context='adhoc')
    app.run(debug=True,port=5000,host="0.0.0.0")