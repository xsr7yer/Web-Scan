import os
import importlib
import requests
from concurrent.futures import ThreadPoolExecutor
from lib.core.get_target import geturl
from lib.core.display import display
import lib.config.config as config

class scan:
    def __init__(self, target_dict,target, module, way):
        self.module = module
        self.way = way
        self.target_dict = target_dict
        self.display = display(target)
    
    def run(self):
        with ThreadPoolExecutor(config.thred_num) as executor1:
            executor1.map(self.exp,self.target_dict)

    def exp(self, url):
        exp_module = importlib.import_module('scripts.{}.{}'.format(self.module,self.way))
        port_info = exp_module.poc(url)
        self.display.print_info(url, port_info)
        self.display.log_info(url, port_info)    #如果不需要纪录文件，注释掉这行。