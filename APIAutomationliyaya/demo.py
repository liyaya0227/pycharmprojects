# # # #判断输入的必须是数字
# # # def is_number(input_str):
# # #     if input_str.isdigit():
# # #         print(input_str)
# # #     else:
# # #         raise ValueError("输入的不是数字")
# # # # 使用示例
# # # try:
# # #     input_value = input("请输入：")
# # #     is_number(input_value)
# # # except ValueError as e:
# # #     print(e)
# # class Instrument():
# #     def make_sound(self):
# #         print('不同乐器发出的声音不同')
# # class Erhu(Instrument):
# #     def make_sound(self):
# #         print('二胡的声音')
# # class Paino(Instrument):
# #     def make_sound(self):
# #         print('钢琴的声音')
# # class Volino(Instrument):
# #     def make_sound(self):
# #         print('小提琴的声音')
# #
# # def play(obj):
# #     obj.make_sound()
# #
# # erhu = Erhu()
# # paino = Paino()
# # volion = Volino()
# # play(erhu)
# # play(paino)
# # play(volion)
# from pandas.core.config_init import pc_show_dimensions_doc
#
#
# class Car():
#     def __init__(self,model,no,):
#         self.model = model
#         self.no = no
#
#     def strat(self):
#         print(f'{self.model}启动了')
#     def end(self):
#         print(f'{self.model}熄火了')
#
# class RentCar(Car):
#     def __init__(self,model, no,carcompany):
#         super().__init__(model, no)
#         self.carcompany = carcompany
#
# class HomeCar(Car):
#     def __init__(self, model, no, carhost):
#         super().__init__(model, no)
#         self.carhost = carhost
#
# rentCar= RentCar('出租车一号', 1000,'长安')
# rentCar.strat()
# homeCar= HomeCar('家用汽车', 1002, 'audi')
# homeCar.strat()

# def write_doc(lst):
#     with open('a.csv', 'w', encoding='UTF-8') as file:
#         file.write(','.join(lst))
#
# def read_doc():
#     with open('a.csv', 'r', encoding='UTF-8') as file:
#         s = file.read()
#         lst = s.split(',')
#         print(lst)

# def write_table(lst):
#     with open('a.csv','w',encoding='UTF-8') as file:
#         for item in lst:
#             file.writelines(item)
#             file.writelines('\n')
#
# def read_table():
#     data = []
#     with open('a.csv','r',encoding='UTF-8') as file:
#         lst = file.readlines()
#         print(lst)
#         for item in lst:
#             lst_new = item[0:len(item)-1].split(',')
#             data.append(lst_new)
#         print(data)
#
# if __name__ == '__main__':
#     lst = [
#         ['西瓜','30元','麒麟瓜'],
#         ['葡萄','10元','阳光玫瑰'],
#         ['草莓','50元','红颜']
#     ]
#     write_table(lst)
#     read_table()

# import random
#
# # 生成一个9位的16进制数
# hex_number = f'{random.getrandbits(36):09X}'
# print(hex_number)
#
# numbers = ['{:04d}'.format(i) for i in range(1, 3001)]
#socket服务器创建
import socket
#创建服务器对象，需要传入参数：AF_INET：表示internet连接，SOCK_STREAM：表示tcp连接
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定IP和端口号,bind()传入的数据是元组类型
server_socket.bind(('127.0.0.1', 1111))
#设置最大连接数
server_socket.listen(5)
#等待客户端的tcp连接，是阻塞性的，返回来的数据是元组类型的数据，需要进行解包赋值操作
client_socket,client_addr = server_socket.accept()
#接收数据
info = client_socket.recv(1024).decode('utf-8')
while info!='bye':
    if info!='':
        print('接收到的数据是：', info)
    #准备发送数据
    data = input('请输入要发送的数据：')
    client_socket.send(data.encode('utf-8'))
    #判断数据
    if data=='bye':
        break
    #重新赋值
    info = client_socket.recv(1024).decode('utf-8')

#关闭socket对象
server_socket.close()
client_socket.close()