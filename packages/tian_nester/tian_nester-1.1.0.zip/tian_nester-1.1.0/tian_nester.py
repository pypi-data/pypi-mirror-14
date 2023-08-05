'''这是一个检查list内元素是否为另一个list的模块，利用递归来检查到最远点,这个模块的作用是
打印list,其中可能包括列表'''
def print_lol(the_list,level):
        for i in the_list:
                if isinstance(i,list):
                        print_lol(i,level+1)
                else:
                        for tab_stop in range(level):
                                print("\t")
                        print(i)

			
	
