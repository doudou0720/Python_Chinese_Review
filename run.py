import uuid
import json
from flask import Flask, make_response , render_template , request ,jsonify 
# 创建日志
# 创建应用实例
app = Flask(__name__,template_folder="./templates",static_folder="./static")

# 载入拓展
print("载入拓展...")
try:
    with open("./extensions/index.json","rb") as f:
        ext = json.load(f)
except:
    print("扩展列表存在问题!程序自动终止，请向作者进行反馈!")
    exit(-1)
print(ext)
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
    global ext
    temp = ext["index"]
    temp1 = []
    for i in temp:
        with open("./extensions"+i["path_info"],"rb") as f:
            ext0 = json.load(f)
        temp1.append(ext0)
    return render_template("show_extensions.html",exts=temp1)

@app.route('/extension/<name>')#拓展列表
def show_extensions(name):
    global ext
    temp = ext["index"]
    temp1 = []
    for i in temp:
        if i["name"] == name:
            with open("./extensions"+i["path_info"],"rb") as f:
                ext0 = json.load(f)
    return render_template("show_extensions_more.html",exts=ext0)
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0",ssl_context='adhoc')
