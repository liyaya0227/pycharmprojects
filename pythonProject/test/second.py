#内置函数range()整数
#range(stop)
r = range(10)
print(list(r))
#range(start,stop)
r = range(1,10)
print(list(r))
#range(start,stop,stop)
r = range(1,10,2)
print(list(r))

#判断是否在数列里面
print(10 in r)
print(10 not in r)