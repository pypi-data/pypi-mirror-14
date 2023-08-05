#创建函数sanitize，将数据项中不规则的分隔符统一为“.”，如数据项2-22经过sanitize处理后，变成了2.22

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins,sece) = time_string.split(splitter)
    return(mins + '.' + sece)

#创建函数count，用于统计每个人最好的前3个成绩

def count(name):
    try:
        with open(name) as name_file:
            data = name_file.readline()
            name = data.strip().split(',')
            print(sorted(set([sanitize(each) for each in name]))[0:3])
            
    except IOError as err:
        print('IOError file:' + str(err))
        return(None)

#打印出每个人前3好的成绩

list = ['james.txt','julie.txt','mikey.txt','sarah.txt']
for each in list:
    count(each)

