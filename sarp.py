# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:57:15 2017

@author: liuya
"""
        
import netifaces
import winreg as wr
import sys
import subprocess

def usage():
    print('''
Copyright 2017, 自足网络 nexfi.cn
 
需要管理员权限, 以下命令有效:
10.0.0.1 40-8d-5c-7b-b6-71     - IP / MAC 绑定
10.0.0.1 0                     - 清除 IP / MAC 绑定
    ''')

def get_connection_name_from_guid(iface_guids):
    iface_names = ['(unknown)' for i in range(len(iface_guids))]
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(iface_guids)):
        try:
            reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
            iface_names[i] = wr.QueryValueEx(reg_subkey, 'Name')[0]
        except FileNotFoundError:
            pass
    return iface_names

"""
    find    not find
del wrong   right
add right   wrong
"""
def checkOut(argv):
    isDel = argv[1] == '0'
    isFind = False
    out = subprocess.getoutput('arp -a')
    lines = out.splitlines()
    for l in lines:
        if l.find(argv[0]) != -1 and l.find('静态') != -1:
            if isDel:
                isFind = True
            elif l.find(argv[1]) != -1:
                isFind = True
                
    if isDel ^ isFind:
        print('执行成功')
    else:
        print('执行失败, 请确认管理员权限')
        
# netsh interface ipv4 add neighbors "以太网" 10.0.0.222 40-8d-5c-7b-b6-71
# netsh interface ipv4 del neighbors "以太网"  10.0.0.222
def main(argv=None):
    x = netifaces.interfaces()
    ifnames = get_connection_name_from_guid(x)
    
    for ifname in ifnames:
        cmd = 'netsh interface ipv4 '
        if argv[1] == '0':
            cmd += 'del neighbors "%s" %s' %(ifname, argv[0])
        else:
            cmd += 'add neighbors "%s" %s %s' %(ifname, argv[0], argv[1])
        subprocess.getoutput(cmd)
    
    checkOut(argv)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    else:
        main(argv=sys.argv[1:])

