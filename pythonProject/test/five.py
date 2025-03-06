#列表
#列表是按顺序存储的
#列表按索引映射唯一数据
#列表可以存储重复数据
#列表可以存储多种类型数据
#列表根据需要动态分配和回收内存

'''创建列表的第一种方式：使用【 】'''
lst = ['hello', 'world', 98, 100, 'good', 'beautiful', 33]

'''创建列表的第二种方式：使用list（）函数'''
lst2 = list(['hello', 'world', 98])

#index()函数，在指定范围内查找元素的索引，或者在指定的位置上查找元素的索引
print(lst.index('hello'))
print(lst2.index('hello', 0, 3))

#获取列表中的指定元素
print(lst[2])

#获取列表中的多个元素——切片操作 列表名：【start:stop:step】
'''print(lst[1:3])
print(lst[1:3:])
print(lst[2:6:2])
print(lst[:6:2])'''

#列表元素的判断及遍历
'''print(33 in lst)
for item in lst:
    print(item)
'''
#列表元素的添加操作
#append()在列表末尾添加一个元素
lst3 = [10, 20, 30, 40, 50]
lst3.append('hello')
print(lst3)
#extend()在列表末尾添加多个元素
lst4 = ['love', 'is', 'beautiful']
lst3.append(lst4)
print(lst3)
lst3.extend(lst4)
print(lst3)
#insert()在列表的任意位置插入元素
lst3.insert(2, 'deam')
print(lst3)
#切片操作: 在列表的任意位置至少添加一个元素
lst3[3:] = lst4
print(lst3)

#从列表中移除元素