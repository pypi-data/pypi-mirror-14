"""the programm that displays a list,
   or the list of the list, by invoke the same function."""


def print_lol(the_list ):
    for item in the_list:
        if(isinstance(item, list)):
           print_lol(item)
        else:
           print(item)

