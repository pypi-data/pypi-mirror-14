#使用pickle方法时需要先导入
import pickle

#1、【根据一定的规则生成一份数据，这里把1到100存入一个列表中。】

List = []
for num in range(100):
    List.append(num+1)


#2、【将列表中的数据存入到文件list_data.txt中】


try:
    ##将数据存入到文件中的方式有好多种，这里介绍三种。
    '''
    ##方法一:
    data=open('list_data.txt','w')#以“写”的方式打开将要写入的文件，赋值给一个“文件变量”
    print(List,file=data)#将List中的数据赋值给“文件变量”data
    data.close()#数据存入到文件中后需要将“文件变量”data关闭，不然数据不会写到文件list_data.txt中

    ##方法二：
    with open('list_data.txt','w') as data:#使用with as操作文件，无需关心“文件变量”是否关闭，系统会自动关闭它
        print(List,file=data)
    '''
    ##方法三：
    with open('list_data.txt','wb') as data:#使用批pickle时，open里面写入方式需要用‘wb’，不然数据无法写入到文件
        pickle.dump(List,data)
    
except IOError as err:#打印IO错误
    print('File error:' + str(err))

except pickle.PickleError as perr:#打印pickle错误
    print('Pickling error:' + str(perr))


#3、【读取文件list_data.txt中的数据，将其赋值给变量out】

out = []#新建一个空列表，用于存储从文件list_data.txt中读取的数据
try:
    '''
    ##从文件中读取数据的方式有好多种，这里介绍三种。
    
    ##方法一:
    data = open('list_data.txt','r')#以“只读”的方式打开文件，赋值给一个“文件变量”
    for out in data:
        print(out,end='')#逐个读取其中的数据到变量out
    data.close()#从文件读取数据完成后需要将“文件变量”data关闭，不然此文件中的数据会一直在内存中，且此文件会一直被占用

    ##方法二：
    with open('list_data.txt','r') as data:#使用with as操作文件，无需关心“文件变量”是否关闭，系统会自动关闭它
        for out in data:
            print(out,end='')
    '''
    ##方法三：
    with open('list_data.txt','rb') as data:#因为前面存数据的时候使用的open方式是‘wb’，所以读取的时候需要使用‘rb’
        out = pickle.load(data)
        print(out,end='')

except IOError as err:#打印IO错误
    print('File error:' + str(err))

except pickle.PickleError as perr:#打印pickle错误
    print('Pickling error:' + str(perr))










 
