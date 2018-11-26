import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def check_file(url):
    url = 'http://'+url
    try:
        f = requests.get(url, timeout=config.time_out)
    except:
        return 0

    if (f.status_code == 200 or f.status_code == 403) and len(f.text) > 0:
        s = requests.get(url+'page_test', timeout=config.time_out) #检测是否是网站自己写的404页面,或者是误报
        if len(s.text) in range(len(f.text)-3,len(f.text)+10):     
            return 0
        else:
            return 1


def poc(url):
    poc_type = 'tools:backfile'

    ports = ['80']
    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)

    with open('./data/dict/backfile','r') as f:
        files = f.readlines()
    
    for port in ports:
        port_info[port] = [0,poc_type,'']
        
        for backfile in files:
            backfile = backfile.strip()
            file_path = url+':'+port+backfile
            if(check_file(file_path)):
                port_info[port] = [1,poc_type,port_info[port][2]+'|'+backfile]
        
        if(port_info[port][2]==''):
            port_info[port][2]='Not found'
    
    return port_info


        