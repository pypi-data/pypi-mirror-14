#
# search engine for the Bible
#

from pybible.Bible import Bible
from pybible.simple import simple_search


def search_simply(word_or_phrase_list, cased_search = False):
    '''
    Searches Bible loosely for terms in list.
    Finds verses with all serach terms present.
    
    Returns list of index numbers.
    '''
    searches = word_or_phrase_list    # converts to search eventually
    search = []
    results = []
    index = 0

    # treat search terms first. Slows down entire search if in for-loop
    if not cased_search:
        for ss in searches:
            search.append(ss.casefold())
    else:
        search = searches

    for line in Bible:

        # take text section
        zone = line[11:]

        # cause casefolding
        if not cased_search: s = zone.casefold()
        else: s = zone

        # get search results
        seen = simple_search(s,search)
                
        # confirm all items have 'True' attribute
        hatch = True    
        for each in seen:
            if not each:
                hatch = False
                break

        # pass result only if all items attributed 'True'
        if hatch:
            results.append(index)

        index += 1
    
    return results
