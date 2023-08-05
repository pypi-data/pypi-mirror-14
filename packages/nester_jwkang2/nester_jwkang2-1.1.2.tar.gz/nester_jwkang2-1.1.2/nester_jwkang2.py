"""This is the "nester.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""
from __future__ import print_function
import sys

def print_all_items(items, ident=False, level=0, fh=sys.stdout):
    """This is the standard way to
     include a multiple-line comment in
     your code."""
    for each_line in items:
        if ident == True:
            if isinstance(each_line, list):
                print_all_items(each_line, True, level+1, fh)
            else:
                for tab in range(level):
                    print("\t", end='', file=fh)
                print(each_line, True, file=fh)
        else:
            print(each_line, file=fh)

if __name__ == '__main__':
    movies = [
        "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
         ["Graham Chapman",
         ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

    print_all_items(movies, ident=True)
