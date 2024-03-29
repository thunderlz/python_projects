import socket
import threading
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9990))
s.listen(5)
print('Waiting for connection...')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    # print(type(addr),len(addr))
    with open('/home/leizhen/socket_recv','at') as f:
            f.write('{}:{}'.format(addr[0],addr[1]))
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        print(data.decode('utf-8'))
        with open('/home/leizhen/socket_recv','at') as f:
            f.write(' '+data.decode('utf-8'))

    sock.close()
    print('Connection from %s:%s closed.' % addr)
    

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
