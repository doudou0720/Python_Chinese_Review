from flask import render_template,request,Flask
import os,re,logging,json


letters = "/[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ()'\"-.\n]/g"
extension_logger = logging.Logger
run_dir = ""
json_info = {}
# from run import app
app = Flask

def init(k:Flask,ext_logger:logging.Logger,run_d:str):
    global app ,extension_logger ,run_dir
    app = k
    extension_logger = ext_logger
    run_dir = run_d
    @app.route("/extension/main.basic.english.reading/show_articles")
    def show_articles():
        concert = request.args.get("name")
        with open(f"{os.getcwd()}/data/Articles/English/{concert}.txt","r") as f:
            a = (f.read())
            b = []
            a = re.sub(letters,"",a)
            # print(a)
            a = a.split("\n")
            for i in a:
                b.append(i.split(" "))
            return render_template("extensions/main/english/reading/reading.html",a = b)

    extension_logger.info("Load main.basic.english.reading successfully!")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")