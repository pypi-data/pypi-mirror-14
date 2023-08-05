def printnst (itemlist,tabornot=False,level=0):
    """print nest"""

    for eachitem in itemlist:
        if isinstance(eachitem,list):
            printnst (eachitem,tabornot,level+1)
        else:
            if tabornot:
                for tab in range(level):
                    print("\t",end='')
            print(eachitem)
            
