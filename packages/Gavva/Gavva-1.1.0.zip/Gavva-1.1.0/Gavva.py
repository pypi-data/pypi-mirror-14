def print_gavva(Gavva,level):
    for each_member in Gavva:
        if isinstance(each_member,list):
            print_gavva(each_member,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_member)
    
