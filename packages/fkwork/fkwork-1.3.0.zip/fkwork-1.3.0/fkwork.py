"""This is the "fkwork.py" module and it provides one function called print_lol
which prints lists the may or may not include nested list."""

movies =['work',1975,'woaik',1976,['milk','mik',['wait','yuyu']]]

def print_lol (the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance (each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_item)
print_lol(movies,4)
        
