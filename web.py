from flask import Flask, render_template, redirect, url_for, request
from generate import Generator
import argparse, os

class ColorfulPrint(object):# {{{

    """Docstring for ColorfulPrint. """

    def __init__(self):
        """nothing needs to be define """
        self.colors = {
            'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
            'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,
        }

    def trans(self, *args):
        s = ' '.join(map('{}'.format, args))
        s = s.replace('(##)', '\033[0m')
        s = s.replace('(#)', '\033[0m')
        for color, value in self.colors.items():
            color_tag = '(#%s)'%color
            s_color_tag = '(#%s)'%color[0]
            s = s.replace(color_tag, '\033[1;%d;m'%value).\
                    replace(s_color_tag, '\033[1;%d;m'%value)
        s = s + '\033[0m'
        return s

    def err(self, *args):
        return self('(#r)[ERR](#)', *args)

    def log(self, *args):
        return self('(#blue)[LOG](#)', *args)

    def wrn(self, *args):
        return self('(#y)[WRN](#)', *args)

    def suc(self, *args):
        return self('(#g)[SUC](#)', *args)

    def __call__(self, *args):
        print(self.trans(*args))

cp = ColorfulPrint()
# }}}
def get_args():# {{{
    parser = argparse.ArgumentParser(description='IC')
    parser.add_argument('--https', action='store_true', default=False)
    return parser.parse_args()
# }}}
def https():# {{{
    path = 'certificate'
    pub = 'server-cert.pem'
    pri = 'server-key.pem'
    
    if not (os.path.isfile(os.path.join(path, pub)) or\
            os.path.isfile(os.path.join(path, pri))):
        os.system('./certificate/cert.sh')
    return {
        'ssl_context': (
            os.path.join(path, pub),
            os.path.join(path, pri),
        )
    }
# }}}
if __name__ == '__main__':
    params = {}
    args = get_args()
    if args.https:
        params = https()
    g = Generator()
    passwd = g.random(32)
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config['SECRET_KEY'] = g.random(32)




@app.route("/", methods=['GET'])
def index(): 
    code = request.args.get('key', '')
    if code != passwd:
        print(code, passwd)
        return '<p><strong>invalid page</strong></p>'
    html_items = {
        'template_name_or_list': 'index.html',
        'codes': codes,
    }
    return render_template(**html_items)



if __name__ == '__main__':
    ips = g.get_ip()
    port = g.random_port()
    for key, ip in ips.items():
        cp.suc('open (#y){}://{}:{}?key={}'.format(
            'https' if args.https else 'http', 
            '[{}]'.format(ip) if key == 'ipv6' else ip, port, passwd))
    codes = g.generate()
    app.run(host='::', port=port, **params)
    
