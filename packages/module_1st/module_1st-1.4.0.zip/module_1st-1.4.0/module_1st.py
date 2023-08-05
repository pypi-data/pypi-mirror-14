def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
        	if indent:
        		for tab_stop in range(level):
        			print("\t", end='')
        	print (each_item)


# list_test = ['a',1,['b'],'c',['d',['f']],'g']

# print_lol(list_test,True,2)