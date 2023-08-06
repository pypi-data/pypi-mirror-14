# coding=utf8

def fnA(list_a,b_indent=False,level=0):
	for item in list_a:
		if isinstance(item,list):
			fnA(item,b_indent,level+1)
		else:
			if b_indent:
				print("\t"*level,end="")		
			print(item)
			
			
			
