from __future__ import print_function
def print_lol(ref1,level):
        for each_item in ref1:
            if isinstance(each_item,list):
               print_lol(each_item,level+1)
            else:
                for num in range(level):
                    print ("\t",end='')
                print(each_item )

words=["hi","what",["hello","yes",["no"]]]
print_lol(words,1)
            