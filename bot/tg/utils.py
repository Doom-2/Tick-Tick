from typing import List, Tuple


def numerate_cats_tuple(cat_set: List[Tuple]) -> str:
    """
    Converts list of tuple to string with line-by-line output
    [('1', 'var1'), ('23', 'var2'), ('34', 'var3')]
    ________
    1  var1
    23 var2
    34 var 3
    """
    return '\n'.join(map(lambda x: '/' + str(x[0]) + ' ' + str(x[1].replace('#', '%23')), cat_set))


def fix_hash_char(lst: List[str]) -> List[str]:
    """ Replaces the # (hash) character with %23 for pretty output in messenger Telegram"""
    return [sub.replace('#', '%23') for sub in lst]
