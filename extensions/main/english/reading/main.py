from flask import render_template,request,Flask
import os,re,logging,json


letters = "/[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ()'\"-.\n]/g"
extension_logger = logging.Logger
run_dir = ""
json_info = {}
# from run import app
app = Flask

def init(k:Flask,ext_logger:logging.Logger,run_d:str):
<<<<<<< HEAD
    global app ,extension_logger ,run_dir ,json_info
=======
    global app ,extension_logger ,run_dir
>>>>>>> 0e3cd0d7597b538d654da33fe27c8fe4b08a6411
    app = k
    extension_logger = ext_logger
    run_dir = run_d
    with open(run_dir+"/init.json","r",encoding="utf-8") as f:
<<<<<<< HEAD
        json_info = json.load(f)
    @app.route("/extensions/main.basic.english.reading/show_articles")
=======
        json.load(f)
    @app.route("/extension/main.basic.english.reading/show_articles")
>>>>>>> 0e3cd0d7597b538d654da33fe27c8fe4b08a6411
    def show_articles():
        concert = request.args.get("name")
        with open(f"{os.getcwd()}/data/Articles/English/{concert}.txt","r") as f:
            a = (f.read())
            a = re.sub(letters,"",a)
            print(a)
            a = a.split("\n")
<<<<<<< HEAD
            b = []
            for i in a:
                b.append(i.split(" "))
            return render_template(json_info["share_templates"]+"/reading.html",a = b)
=======
            return render_template("reading.html",a = a)
>>>>>>> 0e3cd0d7597b538d654da33fe27c8fe4b08a6411

    extension_logger.info("Load main.basic.english.reading successfully!")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")