
def printLoop(args):
    for item in args:
        if isinstance(item,list):
            printLoop(item)
        else:
            print(item)


