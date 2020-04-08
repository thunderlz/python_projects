import socket
import getpass
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect((sys.argv[1], 9990))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [getpass.getuser().encode('utf-8'), socket.gethostname().encode('utf-8'), 'end'.encode('utf-8')]:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
