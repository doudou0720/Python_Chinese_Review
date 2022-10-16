# 导入Flask类库
from flask import Flask , render_template
import uuid
# 创建应用实例
app = Flask(__name__,template_folder="./templates",static_folder="./static")
def create_uuid():
	return uuid.uuid4().hex
# 视图函数（路由）
@app.route('/test/home')
def index():
	return render_template("home.html")
# 启动实施（只在当前模块运行）

if __name__ == '__main__':
	app.run(debug=True,port=80,host="0.0.0.0")
