"""This is the 'nester.py' module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""


def print_lol(the_list, level):
    """This function takes a positional argument called 'the_list', which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line.
    A second argument called “level" is used to insert tab-stops when a nested list
    is encountered."""

    for item in the_list:
        if isinstance(item, list):
            print_lol(item, level + 1)
        else:
            for tab_stop in range(level):
                print('\t', end="")
            print(item)


movies = ['The Holy Grail', 1975, 'Terry Jones & Terry Giliam', 91,
          ['Graham Chapman',
           ['Michael Palin', 'John Cleese', 'Teryy Giliam', 'Eric Idle', 'Terry Jones']]]

print_lol(movies, 0)