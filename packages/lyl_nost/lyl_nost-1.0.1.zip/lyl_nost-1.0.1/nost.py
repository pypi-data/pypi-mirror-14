'''这是LYL—nest.py模块，提供了一个名为check的函数，用来打印整张列表，其中包含或不包含嵌套列表'''
def check(listi ,num=0):
	'''这个函数有一个位置函数，会将列表中的每一项按行输出，而且各占一行'''
	for i in listi:
		if isinstance(i,list):
			check(i,num+1);
		else:
                    for o in range(num):
                        print("\t",end='');
                    print(i)
