#!/usr/local/bin/python3.5
movies=['The Holy Grail',1975,'Terry Jones & Terry Gilliam',91,
        ['Graham Chapman',['Michael Palin','John Cleese','Terry Gilliam','Eric Idle','Terry Jones']]]
""" This ia a way to display the content of the list that
 contains serveral childlist"""
def print_list(arg_list,arg1=0,indent=False):
	for item in arg_list:
		if isinstance(item,list):
			print_list(item,arg1+1,indent)
		else:
			if indent:
				'''for num in range(arg1):
					print("\t",sep='',end='')'''
				print("\t"*arg1,end='')
			print(item)

#print_list(movies,indent=True)
