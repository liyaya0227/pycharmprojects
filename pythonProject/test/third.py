#循环语句 while ， for_in
sum = 0
a = 1
'''while a < 100:
    a += 1
    sum += a
print(sum)'''

'''while a <= 100:
    if a % 2 == 0:
        sum += a
    a += 1
print(sum)'''

# for-in 循环
# for 自定义变量  in  可迭代对象 //将可迭代对象的值一次赋值给自定义变量
# for _  in 可迭代对象 //在循环体中不需要使用到自定义变量，可以使用_

for item in range(101):
    if item % 2 == 0:
        sum += item
print(sum)

for i in range(1,1001):
    ge = i%10
    shi = i//10%10
    bai = i//100
    if ge**3 + shi**3 + bai**3 == i:
        print(i)

#continue 跳出本次循环，
#break 终止循环
