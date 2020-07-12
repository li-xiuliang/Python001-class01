import os
import socket
from multiprocessing.pool import Pool
from multiprocessing import Manager
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
import argparse
import queue
import threading
import re
import json


def ping(s = ()):   # s = (q, l, ip, result_thread)
    q, l, ip, result_thread= s
    if os.name == 'nt':
        cmd = f'ping -n 2 -w 1 {ip}'
    elif os.name == 'posix':
        cmd = f'ping -c 2 -w 1 {ip}'
    else:
        raise os.error('未知操作系统')
    if q:
        l.acquire()
        ping_result = os.system(cmd)
        if ping_result:
            print(f'{ip} NO')
            q.put((ip, 'NO'))
        else:
            print(f'{ip} OK')
            q.put((ip, 'OK'))
        l.release()
    else:
        if l:
            l.acquire()
            ping_result = os.system(cmd)
            if ping_result:
                print(f'{ip} NO')
                result_thread.append((ip, 'NO'))
            else:
                print(f'{ip} OK')
                result_thread.append((ip, 'OK'))
            l.release()
        else:
            ping_result = os.system(cmd)
            if ping_result:
                print(f'{ip} NO')
                return (ip, 'NO')
            else:
                print(f'{ip} OK')
                return (ip, 'OK')

def tcp_check(s = ()): # s = (q, l, ip, port, result_thread)
    q, l, ip, port, result_thread = s
    if q:
        l.acquire()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f'{port} OPEN')
            q.put((port, 'OPEN'))
        else:
            print(f'{port} CLOSE')
            q.put((port, 'CLOSE'))
        l.release()
    else:
        if l:
            l.acquire()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f'{port} OPEN')
                result_thread.append((port, 'OPEN'))
            else:
                print(f'{port} CLOSE')
                result_thread.append((port, 'CLOSE'))
            l.release()
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f'{port} OPEN')
                return (port, 'OPEN')
            else:
                print(f'{port} CLOSE')
                return (port, 'CLOSE')

def multi_process(func, args = (), tasks = 4, q_thread = []):
    with Pool(processes = tasks) as pool:
        pool.map(func, args)

def multi_thread(func, args = (), tasks = 4):
    with ThreadPoolExecutor(max_workers=tasks) as executor:
        executor.map(func, args)  



def ipv4(s):
    try:
        return str(int(s)) == s and 0 <= int(s) <= 255
    except:
        return False
def isIPv4(IP):
    if IP.count('.') == 3 and all(ipv4(i) for i in IP.split('.')):
        return True
    else:
        return False
def check_ip_ping(s):
    if not s.count('-') == 1:
        return False
    else:
        ip_start, ip_end = s.split('-')
        if not isIPv4(ip_start) or not isIPv4(ip_end):
            return False
        else:
            ips = ip_start.split('.')
            ipe = ip_end.split('.')
            for i in range(4):
                if int(ips[i]) > int(ipe[i]):
                    return False
    return True

def get_iplist(s):
    ips = []
    start_ip, end_ip = s.split('-')
    ip_split_start = start_ip.split('.')
    ip_split_end = end_ip.split('.')
    for ip1 in range(int(ip_split_start[0]), int(ip_split_end[0]) + 1):
        for ip2 in range(int(ip_split_start[1]), int(ip_split_end[1]) + 1):
            for ip3 in range(int(ip_split_start[2]), int(ip_split_end[2]) + 1):
                for ip4 in range(int(ip_split_start[3]), int(ip_split_end[3]) + 1):
                    ips.append('.'.join([str(ip1), str(ip2), str(ip3), str(ip4)]))
    return ips


class InputError(Exception):
    def __init__(self, arg):
        self.args = arg

def validate_file(file):
    file_r = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(file_r, "_", file)
    if not new_title.endswith('.json'):
        return new_title + '.json'
    return new_title

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest = 'num_par', type = int, action = 'store', default = 1, help = '同时并发数')
    parser.add_argument('-f', dest = 'method', action = 'store', choices=['ping', 'tcp'], help = '测试方式， ping tcp')
    parser.add_argument('-i', '--ip', dest = 'addr_ip', action = 'store', help = 'IP 地址，示例：192.168.0.1-192.168.0.100')
    parser.add_argument('-w', dest = 'file',  action = 'store', help = '存储文件名')
    parser.add_argument('-m', dest = 'multi',  action = 'store', default = 'proc', choices=['proc', 'thread'], help = '多进程或者多线程： proc thread')
    parser.add_argument('-v', dest = 'run_time',  action = 'store_true', help = '显示运行时间')
    args = parser.parse_args()
    return args.__dict__

if __name__ == '__main__':
    args = arg_parse()
    begin = time.time()
    q = Manager().Queue()
    result = []
    if args['addr_ip']:
        s = args['addr_ip']
        if not check_ip_ping(s) and not isIPv4(s):
            raise InputError(['非法 IP 输入'])
    else:
        raise InputError(['必须输入IP'])
    if args['method'] == 'ping':
        if '-' in s:
            ips = get_iplist(s)
        else:
            ips = [s,]
        if args['num_par'] == 1:
            for ip in ips:
                result.append(ping(('', '', ip, [])))
        else: 
            # if not args['multi']:
            #     raise InputError(['n 大于0的时候，需要 multi 参数 [proc, thread]'])
            cpus = multiprocessing.cpu_count()
            tasks = min(cpus, args['num_par'])
            l_process = Manager().Lock()
            l_thread = threading.RLock()
            func = ping
            if args['multi'] == 'proc':
                multi_args = ((q, l_process, ip, result) for ip in ips)
                multi_process(func, args = multi_args, tasks = tasks)
            elif args['multi'] == 'thread':
                multi_args = (('', l_thread, ip, result) for ip in ips)
                multi_thread(func, args = multi_args, tasks = tasks)
    elif args['method'] == 'tcp':
        ip = args['addr_ip']
        if args['num_par'] == 1:
            for port in range(1, 3):
                result.append(tcp_check(('', '', ip, port, [])))
        else:
            # if not args['multi']:
            #     raise InputError(['n 大于0的时候，需要 multi 参数 [proc, thread]'])
            cpus = multiprocessing.cpu_count()
            tasks = min(cpus, args['num_par'])
            q = Manager().Queue()
            l_process = Manager().Lock()
            l_thread = threading.RLock()
            func = tcp_check
            port_max = 1025
            if args['multi'] == 'proc':
                multi_args = ((q, l_process, ip, port, result) for port in range(port_max))
                multi_process(func, args = multi_args, tasks = tasks)
            elif args['multi'] == 'thread':
                multi_args = ((q, l_thread, ip, port, result) for port in range(port_max))
                multi_thread(func, args = multi_args, tasks = tasks)
    times = time.time() - begin
    if args['run_time']:
        print('运行时间：{:.2f}s'.format(times))
    if q:
        while not q.empty():
            result.append(q.get())
    if args['file']:
        file_name = validate_file(args['file'])
        dump_data = json.dumps(result)
        with open(file_name, 'w') as f:
            json.dump(dump_data, f)

    
            
    



        
            
            
    

