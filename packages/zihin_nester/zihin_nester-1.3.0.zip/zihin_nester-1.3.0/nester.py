def print_lol(the_list,indent=False,level=0):
        for item in the_list:
                if isinstance(item,list):
                        print_lol(item,indent,level+1)
                else:
                        if indent==True:
                                #for tab_stop in range(level):
                                        #print('\t',end='')
                                        print('\t'*level,end='')
                        print(item)
