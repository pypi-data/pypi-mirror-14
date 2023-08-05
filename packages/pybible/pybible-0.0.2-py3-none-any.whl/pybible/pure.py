#
#   functions for the pure search.
#


def cleane(s,e):
    ''' clean element from string. '''

    s = s.partition(e)

    # break operations
    if s[2] == '': return str(s[0])

    # continue taking out commas
    s = s[0] + s[2]

    return cleane(s,e)

def clean(s):
    ''' Complete clean, even punctutation. '''
    punc = [':', '.', '\n', ',', ';', '?', "'", '(', ')', '!', '-', '"']
    s = s.strip()
    for e in punc:
        s = cleane(s,e)
        
    return s


def pure(word, s):
    ''' Determine that nothing else but s is present in word.'''
    word = clean(word)
    a = word.partition(s)
    if a[0] == '' and a[2] == '' and a[1].find(s) == 0:
        return True

    return False

def is_pure(sentence, word):
    ''' Finds word in sentence from index, sees if the word is alone.'''
    # split into words
    look = sentence.split()
    for e in look:
        # find word with target
        if e.find(word) >= 0 and pure(e,word):
            return True
        
    return False


def pure_search(s,search):
    '''
    Does a pure word search for each item in search.
    '''
    seen = []
    for item in search:
        # omit blanks
        if item == '': continue
        # decapitalise search terms
        item = item.casefold()
        if item in s and ispure(s, item):
            seen.append(True)
        else:
            seen.append(False)

    return seen
