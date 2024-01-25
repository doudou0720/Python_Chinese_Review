import sqlite3
import flask
from flask import render_template,request,Flask
import sys,os,re

sys.path.append("../../../../")
letters = "/[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ()'\"-.\n]/g"
# from run import app
app = Flask(__name__,template_folder=f"{os.getcwd()}/templates/extensions/main/english/reading/",static_folder=f"{os.getcwd()}/static")


@app.route("/extension/main.basic.english.reading/show_articles")
def show_articles():
    concert = request.args.get("name")
    with open(f"{os.getcwd()}/data/Articles/English/{concert}.txt","r") as f:
        a = (f.read())
        a = re.sub(letters,"",a)
        print(a)
        a = a.split("\n")
        return render_template("reading.html",a = a)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")