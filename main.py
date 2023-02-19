import uuid
import json
from flask import Flask, make_response , render_template , request ,jsonify 
# 创建日志
# 创建应用实例
app = Flask(__name__,template_folder="./templates",static_folder="./static")
# 创建变量用于计数
TOTAL = 5
count = 0
# 视图函数（路由）5
@app.route('/home')#主页
def index():
    """
    主页展示函数
    :input None
    :return string
    """
    return render_template("home.html",user_name = "test")
count += 1
@app.route('/about')#关于
def about():
    """
    关于页展示函数
    :input None
    :return string
    """
    return render_template("about.html")
count += 1
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
count += 1
@app.route('/whiledoing')#任务进行时
def while_doing():
    return render_template("whiledoing.html")
count += 1
@app.route('/settings')#设置
def settings():
    return render_template("settings.html")
@app.route('/get_task_json',methods=['POST'])#后台:获取任务json
def get_task_json():
    try:
        with open(
            "./data/Tasks/{name}.json".format(
                name=request.form["id"]
            ),
            "r",
            encoding="utf-8"
        ) as f:
            return jsonify(json.dumps((f.read()).strip("\n")))
    except Exception as Error_in_main:
        return make_response("<h2>Error!See the log file in flask.log</h2>", 404)
count += 1
del TOTAL , count
def create_uuid():
    return uuid.uuid4().hex
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0",ssl_context='adhoc')
