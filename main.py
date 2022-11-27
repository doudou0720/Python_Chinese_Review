# 导入Flask类库
import uuid , os
from flask import Flask , render_template , request
# 创建应用实例
print(os.chdir)
app = Flask(__name__,template_folder="./templates",static_folder="./static")
def create_uuid():
    return uuid.uuid4().hex
# 视图函数（路由）
@app.route('/test/home')
def index():
    return render_template("home.html",user_name = "test")
# 启动实施（只在当前模块运行）
@app.route('/deal')
def deal():
    type = request.args.get("type")
    return "OK"
if __name__ == '__main__':
    app.run(port=80,host="0.0.0.0")
