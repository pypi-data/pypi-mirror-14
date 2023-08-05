def aks(the_list):
    for i in the_list:
        if isinstance(i,list):
            aks(i)
        else:
            print(i)
            
