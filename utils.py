#defining a minmax function for use as fuzzy system
def minmax(minn, midd, maxx):
    return min(maxx, max(minn, midd))

#convert from binary
def convert(some_list):
    mylist = some_list
    mystring = ''.join(str(i) for i in mylist)
    return int(str(mystring),2)