"""
    A Simple Printer Of Nested Lists
    agrs: list of dis
    step: tabs count of dis
"""
def printLoop(args,step):
    for item in args:
        if isinstance(item,list):
            printLoop(item,step+1)
        else:
           for tab_step in range(step):
              print("\t",end='')
           print(item)

