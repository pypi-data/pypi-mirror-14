#
# searches for the bible chapter and verse.
#

from pybible.Bible import Bible
from pybible.functions import Books, tonumber, tonumberfull,interpret
from os import system

'''
Functions
'''

def numerise(label, full = False):
    '''
    Process the book, chapter, verse label e.g. Ge1:1.
    Returns a tuple of integers for (book number, chapter, verse).
    '''
    index = 0
    legit = False
    # looks for chapter digit
    for i in range(1,len(label)):
        if label[i].isdigit():
            index = i
            legit = True
            break

    if not legit: return False

    # split book and chapter/verse apart
    book = label[:index]
    chaver = label[index:]

    # process book to number
    if full:
        book = tonumberfull(book)
        
    else:
        book = tonumber(book)

    if not book: return False


    # split chapter and verse
    chaver = chaver.partition(':')
    chapter = int(chaver[0])
    verse = int(chaver[2])

    return (book,chapter,verse)


def code(Tuple):
    '''
    Turns book,chapter,verse tuple into searchable string.
    Returns a searchable string.
    '''
    book = str(Tuple[0])
    chapter = str(Tuple[1])
    verse = str(Tuple[2])

    book = book.zfill(2)
    chapter = chapter.zfill(3)
    verse = verse.zfill(3)

    return book + ':' + chapter + ':' + verse


def search(Code):
    '''
    Searches the searchable 'barcode' in the bible.
    Returns index number of the verse.
    '''
    found = False
    verse = ''
    index = 0
    for line in Bible:
        code = line[:10]
        if code == Code:
            found = True
            break
            
        index += 1

    # control for unfound
    if not found: return None
    
    return index


'''
Main
'''

def getindex(verse, full = False):
    """ Result is None if not found."""
    nume = numerise(verse, full)
    if not nume: return None
    else:
        tup = code(nume)
        index = search(tup)

    return index
   
