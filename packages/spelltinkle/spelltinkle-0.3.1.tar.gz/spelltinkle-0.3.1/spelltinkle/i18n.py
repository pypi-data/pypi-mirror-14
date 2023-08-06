__all__ = ['_']

da = {
    'year': 'år',
    'years': 'år',
    'mon': 'man',
    'tue': 'tir',
    'wed': 'ons',
    'thu': 'tor',
    'fri': 'fre',
    'sat': 'lør',
    'sun': 'søn',
    'may': 'maj',
    'oct': 'okt',
    'modified': 'ændret'}

de = {
    'year': 'Yahr',
    'years': 'Yahre',
    'mon': 'Mon',
    'tue': 'Die',
    'wed': 'Mit',
    'thu': 'Don',
    'fri': 'Fre',
    'sat': 'Sam',
    'sun': 'Son'}


dictionary = None


def set_language(lang=None):
    global dictionary
    dictionary = da
    

def _(word):
    return dictionary.get(word, word)
