import uuid , os ,json
from flask import Flask , render_template , request ,jsonify
# 创建应用实例
app = Flask(__name__,template_folder="./templates",static_folder="./static")
def create_uuid():
    return uuid.uuid4().hex
# 视图函数（路由）
@app.route('/home')#主页
def index():
    return render_template("home.html",user_name = "test")
@app.route('/about')#关于
def about():
    return render_template("about.html")
@app.route('/history')#历史
def history():
    return render_template("history.html",historys=[{"title":"Test","description":"Test,too","id":114514},{"title":"Test2","description":"Test2,too","id":5201314}])
@app.route('/whiledoing')#任务进行时
def while_doing():
    return render_template("whiledoing.html")
@app.route('/get_task_json',methods=['POST'])#后台:获取任务json
def get_task_json():
    try:
        with open("./data/Tasks/{name}.json".format(name=request.form["id"]),"r",encoding="utf-8") as f:
            return jsonify(json.dumps((f.read()).strip("\n")))
    except Exception as e:
        return "Error:"+str(e) , 404
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    app.run(debug=True,port=80,host="0.0.0.0")
