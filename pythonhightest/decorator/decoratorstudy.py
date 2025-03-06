'''学习装饰器之前必须掌握的概念'''

'''
1、函数即变量：函数即变量，任何变量名都是指向变量值的内存地址
2、高阶函数：接受函数名作为形参、返回值中包括函数名
3、装饰器=高阶函数+嵌套函数
'''

'''
函数可以直接被调用，也可以作为变量进行赋值
'''
def boo():
    print('boo')

a = boo
a()
#函数即变量，任何变量名都是指向变量值的内存地址
#函数的本质是一串字符串，保存在内存空间中，函数名只是指向该内存空间的地址

'''
高阶函数
a = gf(func) #函数名作为变量赋值
a()
'''

'''
嵌套函数：通过def关键字定义在另一个函数中的函数
'''
import time
def foo():
    print('foo')

def gf(func):
    def boo():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f'func{func}执行的时间为: {end_time - start_time}')
    return boo
foo = gf(foo)
foo()

#简化调用方式，使用@标识符
import time
def gf(func):
    def boo():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f'func{func}执行的时间为: {end_time - start_time}')
    return boo
@gf
def foo():
    print('foo')

foo()
'''
常见的装饰器类型：
1、被装饰函数带参数
2、装饰器本身带参数
3、被装饰函数带返回值
'''

'''
1、被装饰函数带参数
'''
import time
def gf(func):
    def boo(name): #使用不定量参数，来自适应装饰函数的参数（*args，**kwargs）
        start_time = time.time()
        func(name) #使用不定量参数，来自适应装饰函数的参数（*args，**kwargs）
        end_time = time.time()
        print(f'func{func}执行的时间为: {end_time - start_time}')
    return boo
@gf #foo = gf(func) = boo
def foo(name): #被装饰函数带参数
    print('foo',name)

foo('liyaya')
#foo('liyaya', 18)

'''
2、装饰器本身带参数:如果装饰器本身带参数，无法通过直接在装饰器函数参数中直接加参数，需要再嵌套一层函数来解决
'''
import time
def gf(time_type):
    print(time_type)
    def outer(func): #嵌套一层函数，以方便装饰器函数本身接受参数
        def inner():
            start_time = time.time()
            func()
            end_time = time.time()
            print(f'func{func}执行的时间为: {end_time - start_time}')
        return inner
    return outer
@gf(time_type = 'minites') #装饰器本身带参数,相当于：foo = gf(time_type = 'minites')(foo) = inner
def foo():
    print('foo')

foo()

'''
3、被装饰函数带返回值：只需要在最内部调用被装饰函数里面返回被装饰函数的返回值就可以
'''
import time
def gf(time_type):
    print(time_type)
    def outer(func): #嵌套一层函数，以方便装饰器函数本身接受参数
        def inner(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            print(f'func{func}执行的时间为: {end_time - start_time}')
            return res #返回被装饰函数的返回值
        return inner
    return outer
@gf(time_type = 'minites') #装饰器本身带参数,相当于：foo = gf(time_type = 'minites')(foo) = inner
def foo(name):
    print('foo')
    return  name
name = foo('liyaya')
print(name)