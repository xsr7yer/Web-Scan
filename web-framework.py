import importlib
from lib.core.get_target import getip
from lib.core.display import display
from lib.core.scan import scan
from lib.parse.parse import parse,interactive
from scripts.tools.backfile import check_file

# print(check_file('127.0.0.1/1.txt'))

# print(load_dict())

# dict_1 = getip('192.168.1.0-192.168.1.20')
# print(dict_1.ip_dict)

# module = 'jboss'
# way = 'cve-2017-7504'
# scan_moudle = scan(['192.168.57.136'],'pingan.com.cn',module,way)
# scan_moudle.run()

# exp_module = importlib.import_module('scripts.{}.{}'.format(module,way))
# port_info = exp_module.poc('192.168.57.133')
# print(port_info)
# dispaly = display('192.168.57.133',port_info)
# dispaly.print_info()
# dispaly.log_info()
# scan_moudle = scan('pingan.com.cn',module,way)
# scan_moudle.run()

# print(parse())

def main():
    target_dict,args = parse()
    scan_moudle = scan(target_dict,args['target'],args['module'],args['way'])
    scan_moudle.run()

if __name__ == '__main__':
    main()