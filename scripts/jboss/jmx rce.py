import requests
import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def poc(url):
    poc_type = 'jboss:jmx rce'

    ports = ['80','8080']

    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)

    page_info,ports = page_monitor(url, '/invoker/JMXInvokerServlet', poc_type, ports)
    port_info.update(page_info)

    for port in ports:
        try:
            s = requests.get('http://{}:{}/invoker/JMXInvokerServlet'.format(url,port))
        except Exception as e:
            port_info[port] = [0,poc_type,'Conect failed']
        else:
            if "java-serialized-object" in s.headers['Content-Type']:
                port_info[port] = [1,poc_type,'Page exist']
            else:
                port_info[port] = [0,poc_type,'Not work']

    return port_info


#利用工具https://cdn.vulhub.org/deserialization/DeserializeExploit.jar