import time

class display:
    def __init__(self, target):
        self.target = target.replace('/','_')
        with open('./data/log/'+self.target,'a+') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")

    def  print_info(self, url, port_info):
        for port,info in port_info.items():
            if info[0]==1:
                print("[+][{}]-{}:{}-{}".format(info[1],url, port, info[2]))
            else:
                print("[-][{}]-{}:{}-{}".format(info[1],url, port, info[2]))
    
    def log_info(self,url,port_info):
        with open('./data/log/'+self.target,'a+') as f:
            for port,info in port_info.items():
                if info[0]==1:
                    f.write("[+][{}]-{}:{}-{}\n".format(info[1],url, port, info[2]))