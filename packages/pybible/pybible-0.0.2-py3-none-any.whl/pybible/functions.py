#
#   functions: some specific functions.
#


from os import system
from pybible.Indices import Indices
from pybible.Chapters import Chapters
from pybible.Bible import Bible


# books of the Bible in full
Booksfull = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

# books of the Bible abbrevations
Books = ['Ge', 'Exo', 'Lev', 'Num', 'Deu', 'Josh', 'Jdgs', 'Ruth', '1Sm', '2Sm', '1Ki', '2Ki', '1Chr', '2Chr', 'Ezra', 'Neh', 'Est', 'Job', 'Psa', 'Prv', 'Eccl', 'SSol', 'Isa', 'Jer', 'Lam', 'Eze', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nahum', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal', 'Mat', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phi', 'Col', '1Th', '2Th', '1Tim', '2Tim', 'Titus', 'Phmn', 'Heb', 'Jas', '1Pet', '2Pet', '1Jn', '2Jn', '3Jn', 'Jude', 'Rev']


###
# bible book functions
##

def getbook(number):
    '''
    Matches the books of the Bible to their number.
    Returns an abbrevation.
    '''
    
    number = int(number)

    book = Books[number-1]
    
    return book


def tonumber(book):
    '''
    Matches book to their number.
    Returns book number. Returns False if not found.
    '''
    book = str(book)
    
    ctr = 0
    found = False
    for Book in Books:
        ctr += 1
        if Book.casefold() == book.casefold():
            found = True
            break

    if found: return int(ctr)
    else: return False


def tonumberfull(book):
    '''
    Matches book to their number.
    Altered to match full book names.
    Returns book number. Returns False if not found.
    '''
    book = str(book)
    
    ctr = 0
    found = False
    for Book in Booksfull:
        ctr += 1
        if Book.casefold() == book.casefold():
            found = True
            break

    if found: return int(ctr)
    else: return False


def getbookfull(number):
    '''
    Matches books of the Bible to their number.
    Returns the full name.
    '''

    number = int(number)

    book = Booksfull[number-1]

    return book


def showbooks():
    '''
    Print list of books with their index number.
    '''
    for i in range(66):
        print(str(i+1).zfill(2), Books[i].ljust(5), Booksfull[i])
    return


def getchapter(book, chapter):
    """
    Uses Indices list.
    Returns matching book and chapter.
    Returns None if none matched.
    """    
    for i in range(len(Indices)):
        if Indices[i][0] == book and Indices[i][1] == chapter:
            return Indices[i]
    return None


def finalchapter(book):
    '''
    Returns the final chapter(also chapter count) of a book.
    '''
    return Chapters[book - 1][1]


def getverses(current_index, next_index):
    '''
    Produces list of index number and respective bible verses
    from range 'current' until 'next_index'.
    '''
    verses = []
    for i in range(current_index, next_index):
        verses.append([
            i,
            Bible[i][11:],
        ])
    return verses


###
# program  mechanisms
##
def uncode(code, full = False):
    '''
    Uncodes the barcode.
    Returns an abbreviated verse, or full if full=True.
    '''
    # separate elements
    book = int(code[:2])
    chapter = int(code[3:6])
    verse = int(code[7:])

    # simplify
    if full: book = getbookfull(book)
    else: book = getbook(book)

    return book + str(chapter) + ':' + str(verse)
    

def interpret(line, full = False):
    '''
    Returns a verse line with the 'bar code' interpreted to
    book name, chapter and verse.
    '''
    if line == '': return ''
    
    # length of code
    lencode = 10
    
    code = line[:lencode]

    uncoded = uncode(code, full)
    
    simple = uncoded + line[lencode:]

    return simple
