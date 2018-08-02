from flask import Flask, render_template, redirect, url_for, request
from config import cfg
import json, random

s = '0987654321qwertyuioplkjhgfdsazxcvbnmPOIUYTREWQASDFGHJKLMNBVCXZ'
def random_str(n=16):
    return ''.join(random.sample(s, n))
app = Flask(__name__, static_folder='templates', static_url_path='')
app.config['SECRET_KEY'] = random_str()

secret = random_str()
@app.route("/", methods=['GET'])
def index(): 
    code = request.args.get('key', '')
    html_items = {
        'template_name_or_list': 'index.html',
        'msgs': msgs if code == secret else []
    }
    
    return render_template(**html_items)

with open(cfg.data_path, 'r') as f:
    msgs, ipv4, ipv6 = json.load(f)


port = 1235
print('[SUC] open http://%s:%s/?key=%s'%(ipv4, port, secret))
print('[SUC] open http://[%s]:%s/?key=%s'%(ipv6, port, secret))
app.run(host='::', port=port, debug=True)
