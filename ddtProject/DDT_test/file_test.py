#从txt文件中读取内容

#打开文件
file = open('author.txt', 'r', encoding='utf-8')
#读取文件
content = file.read()
#读取文件的内容为str
print(type(content))
#通过分隔符切割字符串，得到每个值
list = content.split(',')
print(list)
#前后字符串包含【】号，采用截取的方式，去除【】号
for author in list[1:-1]:
    #得到的每个值，都带了''号，要把''去掉
    #print(author)
    print(author[2:-1])
#关闭文件
file.close()