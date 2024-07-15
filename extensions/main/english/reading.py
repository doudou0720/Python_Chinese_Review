from flask import render_template,request,Flask,Response
import os,re,logging,json

import requests


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
        concert = request.args.get("id")
        with open(f"{os.getcwd()}/data/Articles/English/{concert}.txt","r") as f:
            a = (f.read())
            b = []
            a = re.sub(letters,"",a)
            # print(a)
            a = a.split("\n")
            for i in a:
                b.append(i.split(" "))
            return render_template("extensions/main/english/reading/reading.html",a = b)
    @app.route("/extension/main.basic.english.reading/append_word")
    def append_word():
        concert = request.args.get("word")
        if concert == None:
            return Response("Cannot Get key 'word'",400)
        concert = requests.get("http://127.0.0.1:5000/extension/main.basic.english.dictionary/get/root?word="+concert)
        if concert.status_code == 200:
            pass
            return Response("Append successfully!",200)
        else:
            return Response("Get root word from '/extension/main.basic.english.dictionary/get/root' failed",500)
    extension_logger.info("Load main.basic.english.reading successfully!")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")