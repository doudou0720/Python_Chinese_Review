import os
import flask

run_dir = os.path.split(__file__)[0]
info_path = run_dir+"/init.json"

def init(k:flask.Flask):
    import main
    main.init(k)