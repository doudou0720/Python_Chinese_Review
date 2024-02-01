from flask import Flask,render_template,request,url_for,redirect
import stardict as sd

app = Flask(__name__,template_folder="./template")
cl = r'.\dict_l.db'

@app.route("/")
def home():
    return render_template("Scratch.html")

@app.route("/s/<word>/")
def seratch(word):
    global cl
    word = str(word)
    ru = sd.StarDict(cl,True).match(word,strip=True)
    other = sd.StarDict(cl,True).query(word)
    ru2 = []
    if other == None:
        print(word)
    for i in ru:
        ru2.append(i[1])
    try:
        c_list_e = other["definition"].splitlines()
    except:
        c_list_e = ["暂无数据"]
    if c_list_e == []:
        c_list_e = ["暂无数据"]
    try:
        c_list_c = other["translation"].splitlines()
    except:
        c_list_c = ["暂无数据"]
    if c_list_c == []:
        c_list_c = ["暂无数据"]
    try:
        exchange = other["exchange"].split("/")
    except:
        exchange = []
    nexchange = []
    if exchange == []:
        nexchange = ["暂无数据"]
    else:
        for i in exchange:
            nexchange.append(i.split(":"))
    try:
        tag = other["tag"].split(" ")
    except:
        tag = []
    return render_template("result.html",rl = ru2,definition = c_list_e,translation = c_list_c,word = other["word"],id = other["id"],exchange = nexchange,tag=tag)

@app.route("/jump/")
def jump():
    a = request.values.get("word")
    return redirect("/s/"+str(a))

if __name__ == "__main__":
    app.run(host="0.0.0.0")