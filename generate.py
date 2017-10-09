import paramiko
import time
import sys
import hashlib
import base64

"""
# macd5.sh
a=`ifconfig | grep wlan0 | md5sum`
b=`ifconfig | grep adhoc0 | md5sum`
echo $a$b | md5sum | sed 's/-//'


# config mesh
config reg reg
    option key b1e703774da75cdd00ddd595217633d2

# on boot process
a=$(sh macd5.sh)
b=$(uci get mesh.reg.key)
if [ $a != $b ];then
# 	bat0 down
fi

"""


def encrypt(key, s):
    b = bytearray(str(s).encode("gbk"))
    n = len(b)  # 求出b的字节数
    c = bytearray(n * 2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")


def decrypt(key, s): 
    c = bytearray(str(s).encode("gbk")) 
    n = len(c) # 计算 b 的字节数 
    if n % 2 != 0 : 
        return "" 
    n = n // 2 
    b = bytearray(n) 
    j = 0 
    for i in range(0, n): 
        c1 = c[j] 
        c2 = c[j+1] 
        j = j+2 
        c1 = c1 - 65 
        c2 = c2 - 65 
        b2 = c2*16 + c1 
        b1 = b2^ key 
        b[i]= b1 
    try: 
        return b.decode("gbk") 
    except: 
        return "failed" 


def sshApply(ip, username, password, cmd):
    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in
    # your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    # initiate SSH connection
    try:
        remote_conn_pre.connect(
            ip, port=19331, username=username, password=password, look_for_keys=False,
            allow_agent=False, timeout=5)
    except Exception as e:
        # print(e)
        print('连接失败 ', ip)
        print('.', end='', flush=True)
        return
    print('\n_________________________________________________________________________________')
    print("SSH connection established to %s " % ip)

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    # print("Interactive SSH session established")

    # Strip the initial router prompt
    remote_conn.send("\n")
    time.sleep(2)
    output = remote_conn.recv(1000)

    # wlan0
    remote_conn.send("macd5.sh\n")
    time.sleep(2)
    output = remote_conn.recv(5000)
    start = output.find(b'\r\n')
    end = output.rfind(b'\r\n')
    sn = output[start:end].decode().strip()
    print(sn)
    snn = base64.b64encode(str(sn+'nexfi').encode())
    print(base64.b64encode(str(sn+'nexfi').encode()))
    print(base64.b64decode(snn))

    # wlan0
    remote_conn.send(cmd + "\n")
    time.sleep(2)
    output = remote_conn.recv(5000)

    start = output.rfind(b'HWaddr')
    end = output.rfind(b'\r\n')
    mac1 = output[start:end].decode().replace('HWaddr', '').strip()

    # adhoc0
    remote_conn.send('ifconfig adhoc0 | grep HWaddr' + "\n")
    time.sleep(2)

    output = remote_conn.recv(5000)
    remote_conn_pre.close()

    start = output.rfind(b'HWaddr')
    end = output.rfind(b'\r\n')
    mac2 = output[start:end].decode().replace('HWaddr', '').strip()

    a = mac2 + '+' + mac1
    m = hashlib.sha256()
    m.update(a.encode())
    # print(m.hexdigest())


    remote_conn_pre.close()


def cmd(option, value='none'):
    return {
        'chanbw': 'cat /etc/config/wireless | grep radio1 ;if [ $? -eq 0 ];\
                  then uci set wireless.radio1.chanbw=' + value + '; else\
                  uci set wireless.radio0.chanbw=' + value + ';fi;\
                  uci commit wireless' if value.isnumeric() and int(value) in [5, 10, 20] else -1,
        'channel': 'cat /etc/config/wireless | grep radio1 ;if [ $? -eq 0 ];\
                  then uci set wireless.radio1.channel=' + value + '; else\
                  uci set wireless.radio0.channel=' + value + ';fi;\
                  uci commit wireless' if value.isnumeric() and int(value) in [2, 3, 4] else -1,
        'show': 'cat /etc/config/wireless | grep radio1 ;if [ $? -eq 0 ];\
                  then uci get wireless.radio1.channel;uci get wireless.radio1.chanbw; else\
                  uci get wireless.radio0.channel;uci get wireless.radio0.chanbw; fi',
        'sn' : 'ifconfig wlan0 | grep HWaddr',       
    }.get(option, -1)


def printHelp():
        print(sys.argv[0], '[IP] [option] [value]')
        print("""栗子:
    ch 192.168.1.1 chanbw 5   # 范围5, 10, 20
    ch 192.168.1.1 channel 3  # 范围2, 3,  4""")


def snGen(ip, username, password):
    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in
    # your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    # initiate SSH connection
    try:
        remote_conn_pre.connect(
            ip, port=19331, username=username, password=password, look_for_keys=False,
            allow_agent=False, timeout=5)
    except Exception as e:
        # print(e)
        print('连接失败 ', ip)
        print('.', end='', flush=True)
        return

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    # print("Interactive SSH session established")

    # Strip the initial router prompt
    remote_conn.send("\n")
    time.sleep(2)
    output = remote_conn.recv(1000)

    # wlan0
    remote_conn.send("macd5.sh\n")
    time.sleep(2)
    output = remote_conn.recv(5000)
    start = output.find(b'\r\n')
    end = output.rfind(b'\r\n')
    sn = output[start:end].decode().strip()

    key = 15
    e = encrypt(key, sn)
    print(e)

    remote_conn_pre.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        printHelp()
    else:
        username = 'root'
        password = 'nexfi'
        ip = sys.argv[1]


        if cmd is not -1:
            snGen(ip, username, password)
        else:
            printHelp()
            print('aa')
