# coding=utf8

def fnA(list_a,level=0):
	for item in list_a:
		if isinstance(item,list):
			fnA(item,level+1)
		else:
			print("\t"*level,end="")		# 可以使用 for in 循环输出 \t
			print(item)
			
			
			
