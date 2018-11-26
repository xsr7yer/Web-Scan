from socket import *
import requests
import lib.config.config as config
import urllib3

#端口存活监测
def port_monitor(url,poc_type,ports):
    port_info = {}
    for port in ports:
        s = socket(AF_INET,SOCK_STREAM)
        s.settimeout(2)
        host = (url, int(port))
        try:
            s.connect(host)
        except Exception as e:
            # print(host)
            # print(e)
            port_info[port] = [0,poc_type,'Port closed']
            ports.remove(port)
    return port_info,ports

#页面存活检测 判断的状态码，http方法（默认为get）传参的时候可以定义
def page_monitor(url,page,poc_type,ports,status_code=[200],method=None,data=None):
    page_info = {}
    for port in ports:
        try:
            if method!=None:
                s = requests.post('http://'+url+':'+port+page, data = data, timeout=config.time_out)
            else:
                s = requests.get('http://'+url+':'+port+page, timeout=config.time_out)
            
            if s.status_code not in status_code:
                page_info[port] = [0,poc_type,'Page not exit']
                # print(page_info)
                ports.remove(port)
        except requests.exceptions.ReadTimeout:
            page_info[port] = [0,poc_type,'Time out']
            ports.remove(port)
        except:
            page_info[port] = [0,poc_type,'Conect failed']
            ports.remove(port)

    return page_info,ports

#https证书错误检测，return False时设置verify=False即可解决证书不安全的问题。
def https_monitor(url,poc_type,ports):
    try:
        s = requests.get(url)
    except requests.exceptions.SSLError:
        return False
    except:
        pass
    return True