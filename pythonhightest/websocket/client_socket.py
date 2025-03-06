import socket
from time import process_time

#创建socket对象,客户端的对象创建不需要传入参数
client_socket = socket.socket()
#连接服务器的ip和端口号，传入的数据类型是元组
client_socket.connect(('127.0.0.1',1111))
print('-----------已经与服务器建立连接----------')
#客户端发送数据
info=''
#循环
while info!='bye':
    data = input('请输入要发送的数据：')
    client_socket.send(data.encode('utf-8'))
    #判断数据
    if data=='bye':
        break
    #接收数据
    info = client_socket.recv(1024).decode('utf-8')
    print('接收到服务器的信息是：',info)

client_socket.close()