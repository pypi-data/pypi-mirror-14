#
# functions for a simple search
#


def simple_search(s, search):
    '''
    Does a simple search on the file line for  the existence of each search item.
    Returns a list of True or False statements.
    True: search item exists, vice versa.
    '''
    seen = []
    for item in search:
        # omit blanks
        if item == '': continue

        # find item
        if item in s:
            seen.append(True)
        else:
            seen.append(False)

    return seen
