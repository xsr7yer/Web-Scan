import socket
import struct
import re
import IPy

class geturl:
    def __init__(self ,url_dict):
        self.url_dict = './data/url_dict/'+url_dict+'.txt'
        self.target_dict = self.get_all()

    def get_all(self):
        with open(self.url_dict,'r') as f:
            ip_list = f.readlines()

        for i in range(len(ip_list)):
            ip_list[i] = ip_list[i].strip()

        for i in range(len(ip_list)):
            try:
                n = ip_list[i].index('[')   #配合这个老哥子域名工具进行枚举https://github.com/cuijianxiong/subdns
            except:
                n = len(ip_list[i])
            ip_list[i] = ip_list[i][0:n].strip()
        
        return ip_list

#输入ip时处理方法 Example：-p 172.16.1.0/24 or -p 172.16.1.0-172.16.1.255
class getip:
    def __init__(self ,ip):
        self.ip = ip
        self.target_dict = self.parse_ip()

    def findIPs(self,start, end):
        ipstruct = struct.Struct('>I')
        start, = ipstruct.unpack(socket.inet_aton(start))
        end, = ipstruct.unpack(socket.inet_aton(end))
        return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end+1)]

    def parse_ip(self):
        ip = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]/?[0-9]?[0-9]?|2[0-4][0-9]/?[0-9]?[0-9]?|[01]?[0-9][0-9]?/?[0-9]?[0-9]?)\b',self.ip)
        if len(ip) not in (1,2):
            print('Example：-p 172.16.1.0/24 or -p 172.16.1.0-172.16.1.255')
            exit()
        elif len(ip)==1:
            ip_list = []
            ip = IPy.IP(ip[0])
            for i in ip:
                ip_list.append(str(i))
            return ip_list
        else:
            return self.findIPs(ip[0],ip[1]) 
