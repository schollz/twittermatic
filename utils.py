
def convertCondensedNum(strnum):
    strnum = str(strnum)
    if 'K' in strnum:
        return int(1000 * float(strnum.split('K')[0]))
    elif 'M' in strnum:
        return int(1000000 * float(strnum.split('M')[0]))
    else:
        return int(strnum)

