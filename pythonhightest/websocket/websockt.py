# -*- coding: utf-8 -*-
"""
@Time ： 2025/3/6 14:58
@Auth ： liyaya
@File ：websockt.py
@IDE ：PyCharm

"""
'''
websocket 就是web socket
问题：1、http是一种传输协议，一次请求和响应之后断开连接
    2、服务端可以向客户端主动推送信息吗？不可以
    3、服务端只能做出响应
    4、为了伪造服务端向客户端推送消息的效果，我们使用轮询和长轮询
诞生了一个新的协议：websocket
    数据格式：连接请求、收发数据
    不断开连接
'''
'''
websocket接口测试：
    1、websocket和http接口的区别：
        1、都是网络接口数据交换协议，都是基于TCP
        2、http每次交互都是一个新的请求（非实时）
           websocket建立长久的网络连接，服务器/客户端可以相互主动发送数据（实时）
    2、实操：
        测试手法不一样，协议不一样
        接口测试：模拟客户端对服务器发起请求
        http接口请求直接调用就可以了
        websocket接口调用测试分为几步：
            1、创建websocket连接
                特定的客户端/代码，这点和http不同
            2、收发数据
                http接口调用，通常不同的接口不同的地址不同的参数
                websocket接口，同一个网络请求，接发不同的数据
            3、关闭连接
    
'''