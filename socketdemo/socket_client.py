import socket
import getpass
import sys
import datetime
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect((sys.argv[1], 9990))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
send_datas = [getpass.getuser().encode('utf-8'), socket.gethostname().encode('utf-8'),
              datetime.datetime.now().strftime('%Y%m%d %H:%M:%S').encode('utf-8')]
try:
    send_datas.append(sys.argv[2])

for data in send_datas:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
