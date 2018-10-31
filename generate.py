# @import: {{{
import os, base64, subprocess, json, time, socket, hashlib
import numpy as np
# }}}


class Generator(object):

    """Docstring for Generator. """

    def __init__(self):
        """init """
        self.ips = None
        self.md5 = hashlib.md5()
        
    def shell(self, cmd):
        """TODO: Docstring for cmd.

        :cmd: command to run
        :returns: shell results

        """
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_f = process.stdout
        error_f = process.stderr
        errors = error_f.read()
        if errors:
            return errors
        return result_f.read()

    def encode(self, data):
        """TODO: Docstring for encode.

        :data: data to encode
        :returns: base64 string

        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')

    def get_ip(self):
        """TODO: Docstring for get_ip.

        :returns: ipv4 & ipv6 address

        """
        if self.ips is None:
            urls = {
                'ipv4': 'https://ipv4.icanhazip.com/',
                'ipv6': 'https://ipv6.icanhazip.com/',
            }
            self.ips = {
                key: self.shell('curl --silent {}'.format(url)).decode('utf-8').strip()
                for key, url in urls.items()
            }
        return self.ips
    def hash(self, s):
        self.md5.update(s)
        return self.md5.hexdigest()

    def random(self, n=16):
        return self.hash(os.urandom(n))


    def random_port(self):
        def is_open(port):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', port))
                s.shutdown(2)
                return True
            except:
                return False
        while True:
            port = np.random.randint(6000, 20000)
            if not is_open(port):
                return port

    def generate(self):
        passwd = self.random()
        port = self.random_port()
        method = "aes-256-cfb"
        ss_profile = {
            "server":"::",
            "server_port": port,
            "local_address": "0.0.0.0",
            "local_port":1080,
            "password": passwd,
            "timeout": 300,
            "method": method,
        }
        ips = self.get_ip()
        date_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        codes = {}
        for ip_key, ip in ips.items():
            code = 'ss://{}'.format(self.encode('{}:{}@{}:{}?Remark={}'.format(
                method, passwd, ip.replace(':', '%3A'), port, '{}@{}'.format(
                    ip_key, date_time).replace(' ', '%20'))))
            codes[ip_key] = code
            print(code)
        return codes
            
            

if __name__ == '__main__':
    g = Generator()
    g.generate()

