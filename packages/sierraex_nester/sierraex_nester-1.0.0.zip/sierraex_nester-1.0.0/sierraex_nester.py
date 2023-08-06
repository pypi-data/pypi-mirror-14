"""comments"""

def print_lol(lst):
    """comments"""
    for i in lst:
        if isinstance(i, list):
            print_lol(i)
        else:
            print(i)
