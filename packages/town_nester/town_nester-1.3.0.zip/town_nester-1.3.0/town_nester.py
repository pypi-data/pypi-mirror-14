"""
    A Simple Printer Of Nested Lists
    agrs: list of dis
    indent: enable dis tab
    step: tabs count of dis
"""
def printLoop(args,indent = False,step = 0):
    for item in args:
        if isinstance(item,list):
            printLoop(item,indent,step+1)
        else:
           if indent: 
               for tab_step in range(step):
                  print("\t",end='')
           print(item)

