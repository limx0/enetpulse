
def maybe_list(l):
    if isinstance(l, (str, int)):
        l = [l]
    return l
