import os, json, random, time, socket, subprocess, re, base64
import numpy as np

from config import cfg

def run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_f = process.stdout
    error_f = process.stderr
    errors = error_f.read()
    if errors:
        return errors
    return result_f.read()


def is_open(port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', port))
        s.shutdown(2)
        return True
    except:
        return False

def random_str(n):
    s = '1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
    x = ''.join(random.sample(s, 16))
    return x

def get_port():
    while True:
        port = np.random.randint(6000, 20000)
        if not is_open(port):
            return port

def get_ip():
    ifconfig = run('ifconfig').decode('utf-8')
    # print(ifconfig)
    re_v4 = re.compile('inet.*?([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)', re.S)
    re_v6 = re.compile('inet6.*?(2400.*?) ')

    v4 = re_v4.findall(ifconfig)[0]
    v6 = re_v6.findall(ifconfig)

    # v4 = run('ifconfig | grep -A 1 "en" | grep broadcast | cut -d " " -f 2 | tr "\\n" " "').decode('utf-8')
    v6 = run('curl --silent http://icanhazip.com').decode('utf-8').replace('\n', '')
    while v4[-1] == ' ':
        v4 = v4[:-1]
    v4 = v4.split(' ')[-1]
    return v4, v6


if __name__ == '__main__':
    random.seed(int(time.time()))
    data = {
        "server":"::",
        "server_port": get_port(),
        "local_address": "0.0.0.0",
        "local_port":1080,
        "password":random_str(16),
        "timeout":300,
        "method":"aes-256-cfb",
        "workers": 1
    }

    out = json.dumps(data)

    ipv4_remark = 'IPv4'
    ipv6_remark = 'IPv6'
    
    ipv4, ipv6 = get_ip()

    date = time.localtime(time.time())
    date = '%d/%02d/%02d %02d:%02d:%02d' % (date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec)

    ipv4_remark = '@'.join([ipv4_remark, date, 'Mac'])
    ipv6_remark = '@'.join([ipv6_remark, date, 'Mac'])
    code_v4 = '{}:{}@{}:{}?Remark={}&OTA=fal'.format(data['method'], \
            data['password'], ipv4, data['server_port'], \
            ipv4_remark.replace(' ', '%20'))

    code_v6 = '{}:{}@{}:{}?Remark={}&OTA=fal'.format(data['method'], \
            data['password'], ipv6.replace(':', '%3A'), \
            data['server_port'], ipv6_remark.replace(' ', '%20'))

    wingy = '{}:{}@{}:{}'.format(data['method'], data['password'],\
            ipv4, data['server_port'])

    
    code_v4 = 'ss://' + base64.b64encode(code_v4.encode()).decode('utf-8')
    code_v6 = 'ss://' + base64.b64encode(code_v6.encode()).decode('utf-8')
    code_wingy = 'ss://' + base64.b64encode(wingy.encode()).decode('utf-8')
    print(code_v4)
    print(code_v6)
    print(code_wingy)
    
    


    with open(cfg.data_path, 'w') as f:
        json.dump([[[code_v4, ipv4_remark], [code_v6, ipv6_remark], [code_wingy, 'wingy']],\
                ipv4, ipv6], f)

    with open(cfg.config_path, 'w') as f:
        json.dump(data, f)

