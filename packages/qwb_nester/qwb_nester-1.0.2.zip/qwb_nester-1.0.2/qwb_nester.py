def print_lol (the_each,lever=0):
    for x in the_each:
        if isinstance (x,list):
            print_lol (x,lever+1)
        else:
            for y in range(lever):
                print ("\t",end='')
            print (x)

aa=[111,222,444,[555,666,[777]]]
print_lol(aa,0)

