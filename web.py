from flask import Flask, render_template, redirect, url_for
from config import cfg
import json

app = Flask(__name__, static_folder='templates', static_url_path='')
app.config['SECRET_KEY'] = 'AKALFHUEWSAiowqjodas'  

@app.route("/")
def index(): 
    html_items = {
        'template_name_or_list': 'index.html',
        'msgs': msgs,
    }
    
    return render_template(**html_items)

with open(cfg.data_path, 'r') as f:
    msgs, ipv4, ipv6 = json.load(f)


port = 1235
print('[SUC] open http://%s:%s'%(ipv4, port))
print('[SUC] open http://[%s]:%s'%(ipv6, port))
app.run(host='::', port=port, debug=True)
