#嵌套语句
'''num_a = int(input('请输入一个整数：'))
num_b = int(input('请输入一个整数：'))
if num_a > num_b:
    print(str(num_a)+'大于'+str(num_b))
else:
    print(str(num_a)+'小于'+str(num_b))'''
num_a = int(input('请输入一个整数：'))
num_b = int(input('请输入一个整数：'))
print(str(num_a)+'大于'+str(num_b) if num_a > num_b else str(num_a)+'小于'+str(num_b))