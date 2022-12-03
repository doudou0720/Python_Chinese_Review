import uuid , os ,json,logging
from flask import Flask , render_template , request ,jsonify
# 创建日志
logging.basicConfig(filename="main.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
# 创建应用实例
logging.info("Create the flask app")
app = Flask(__name__,template_folder="./templates",static_folder="./static")
logging.info("Create webside:")
# 创建变量用于计数
TOTAL = 5
count = 0
# 视图函数（路由）
@app.route('/home')#主页
def index():
    return render_template("home.html",user_name = "test")
count += 1
logging.info("  ({now},{total}):create webside:{name}".format(now=count,total=TOTAL,name="/home"))
@app.route('/about')#关于
def about():
    return render_template("about.html")
count += 1
logging.info("  ({now},{total}):create webside:{name}".format(now=count,total=TOTAL,name="/about"))
@app.route('/history')#历史
def history():
    return render_template("history.html",historys=[{"title":"Test","description":"Test,too","id":114514},{"title":"Test2","description":"Test2,too","id":5201314}])
count += 1
logging.info("  ({now},{total}):create webside:{name}".format(now=count,total=TOTAL,name="/history"))
logging.warning("This website has not completed!")
@app.route('/whiledoing')#任务进行时
def while_doing():
    return render_template("whiledoing.html")
count += 1
logging.info("  ({now},{total}):create webside:{name}".format(now=count,total=TOTAL,name="/whiledoing"))
@app.route('/get_task_json',methods=['POST'])#后台:获取任务json
def get_task_json():
    try:
        with open("./data/Tasks/{name}.json".format(name=request.form["id"]),"r",encoding="utf-8") as f:
            return jsonify(json.dumps((f.read()).strip("\n")))
    except Exception as e:
        logging.error("Something went wrong in '/get_task_json'.See the message below!")
        logging.exception(e)
        return "Error:"+str(e) , 404
count += 1
logging.info("  ({now},{total}):create webside:{name}".format(now=count,total=TOTAL,name="/get_task_json"))
logging.warning("It's only for 'POST' method!")
del TOTAL , count
logging.info("Create other function")
def create_uuid():
    return uuid.uuid4().hex
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    logging.info("Start flask app!")
    app.run(debug=True,port=80,host="0.0.0.0")
