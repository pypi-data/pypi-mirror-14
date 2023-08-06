"""the programm that displays a list,
   or the list of the list, by invoke the same function."""


def print_lol(the_list, level ):
    for item in the_list:
        if(isinstance(item, list)):
           print_lol(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(item)

