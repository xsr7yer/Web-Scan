import argparse
import os
import glob

from lib.core.get_target import getip,geturl

def parse():
    parser =argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group() 
    group.add_argument("-u","--url", required=False,help="-u www.baidu.com")
    group.add_argument("-p","--ip", required=False,help="-p 172.16.10.0/24")

    parser.add_argument("-m","--module",required=False,help="-m weblogic")
    parser.add_argument("-w","--way",required=False,help="-w CVE-2017-10271")

    args = parser.parse_args().__dict__
    
    if (args['url']==None) and (args['ip']==None):
        parser.print_help()
        exit()

    if (args['module']==None) or (args['way']==None):
        args.update(interactive())

    if args['url']!=None:
        target = geturl(args['url'])
        args['target'] = args['url']
    else:
        target = getip(args['ip'])
        args['target'] = args['ip']

    return target.target_dict,args

def interactive():
    dir = './scripts/'

    module_list = os.listdir(dir)
    print("[+]Module_list:")
    for i in range(len(module_list)):
        print('[{}]:[{}]'.format(i+1,module_list[i]))
    
    module_num = input('[*]Chose the module:')
    module = module_list[int(module_num)-1]
    way_list = os.listdir(dir+module+'/')
    print("[+]Script_list:")
    for i in way_list:
        if not i.endswith('.py'):
            way_list.remove(i)

    for i in range(len(way_list)):    
        way_list[i] = way_list[i][:way_list[i].index('.py')]
        print('[{}]:[{}/{}]'.format(i+1,module,way_list[i]))

    way_num = input('[*]Chose the script:')
    way = way_list[int(way_num)-1]

    return {'module':module,'way':way}