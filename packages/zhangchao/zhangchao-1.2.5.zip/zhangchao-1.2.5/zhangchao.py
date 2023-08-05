'''
Created on 2016年3月15日

@author: zsuper

'''
import sys
def print_lol(the_list,ident=False,level=0,fn=sys.stdout):
    #实现功能：将列表有缩进地输出
    for each_line in the_list:
        if isinstance(each_line,list):
            print_lol(each_line,indent,level+1,fn)
        else:
            if indent:
                for tap_stop in range(level):
                    print("\t",end='',file=fn)
            print(each_line,file=fn)   
             

# def sanitize(line):
#     if ':' in line:
#         line.replace(':','.')
#         return(line)
#     #刚才是因为没有返回一个值？？答：还是不行
#     elif '-' in line:
#         line.replace('-','.')
#         return(line)
#     else:
#         return(line)
#         

def sanitize(line):
    #实现功能：将字符串进行标准化，去除：和-，输出合适格式的的字符串
    if ':' in line:
        splitter=':'
    elif '-' in line:
        splitter='-'
    else:
        return(line)
    #return调用之后直接返回，而不会再进行下面的操作？？
    
    (min,sec)=line.split(splitter)
    return(min+'.'+sec) 

def standard(dizhi):
    #输入：一个表示地址的字符串
    #实现功能：将运动数据分为-->姓名，年龄，最好的三个成绩（引用本文件中的sanitize函数）
    #将其分别存进字典中，对应：name、age和score
    #返回一个字典
    try:
        people=[]
        runner={}
        with open(dizhi) as di:
            data=di.readline()
            people=data.strip().split(',')
        
        runner['name']=people.pop(0)
        runner['age']=people.pop(0)
        
        people=sorted([sanitize(line) for line in people],reverse=True)[0:3]
        runner['score']=people
        
        return(runner)
        
        #这里无需创建临时列表，只需要return(data.strip().split(','))
    
#     except IOExcept:
#         return('fucking!!!')

    except IOExcept as ioerr:
        #I/O异常控制
        print('file error:'+str(ioerr))
        return(none)

class AthleteList(list):
    #实现功能：构建继承于list的athletelist
    #本身就是一个list，可以利用本身存储字符串
    def __init__(self,a_name,a_dob=None,a_times=[]):
        #初始化一个类
        list.__init__([])
        self.name=a_name
        self.dob=a_dob
        self.extend(a_times)
    
    def top3(self):
        #筛选出最好的三个成绩
        return sorted(set([sanitize(each) for each in self]))[0:3]

def get_data(filename):
    try:
        with open(filename) as fn:
            data=fn.readline()
        templ=data.strip().split(',')
        return(AthleteList(templ.pop(0),templ.pop(0),templ))
    except IOError as ioerr:
        print('File error:'+str(ioerr))
        return(None)
