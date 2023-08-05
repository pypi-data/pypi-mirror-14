def print_gavva(Gavva):
    for each_member in Gavva:
        if isinstance(each_member,list):
            print_gavva(each_member)
        else:
            print(each_member)
    
