
def to_number_name(num):
    """Converts a number to a number name.
       e.g. 1123 to one thousand one hundred twenty three
       :attr num - an integer
    """

    def xconcat(*strs):
        sep = ' '
        res_str = ''
        for s in strs:
            if s.strip() != '':
                if res_str.strip() != '':
                    res_str += sep + s
                else:
                    res_str = s
        return res_str

    assert type(num) == int, "must provide only integer as an argument"
    assert num >= 0, "number must be non negative"
    num = str(num)
    assert len(num) < 121, "number must be less than or at max 0.9 x 10 ^ 121"
    names = [
                {"0":"zero", "1":"one","2":"two","3":"three","4":"four",
                    "5":"five","6":"six","7":"seven","8":"eight","9":"nine",
                    "10":"ten","11":"eleven","12":"twelve","13":"thirteen",
                    "14":"fourteen","15":"fifteen","16":"sixteen","17":"seventeen",
                    "18":"eighteen","19":"nineteen"},
                {"2":"twenty","3":"thirty","4":"forty",
                    "5":"fifty","6":"sixty",
                    "7":"seventy","8":"eighty","9":"ninety"},
                ["","thousand","million","billion","trillion","quadrillion",
                    "quintillion","sextillion","septillion","octillion",
                    "nonillion","decillion","undecillion","duodecillion",
                    "tredecillion","quattuordecillion","quindecillion",
                    "sexdecillion","septdecillion","octdecillion",
                    "novemdecillion","vigintillion"]
            ]

    place_value_idx = 0
    nump = num[-3:]
    num = num[:-3]

    s = ''
    while len(nump)> 0:
        place_value = names[2][place_value_idx]
        l = len(nump)
        ts  = ''
        if l == 3:
            if int(nump[-2:]) > 0 and int(nump[-2:]) < 20:
                ts = names[0][str(int(nump[-2:]))]
            elif int(nump[-2:]) > 19 and int(nump[-2:]) < 100:
                if nump[2] != '0':
                    ts = xconcat(names[1][nump[1]], names[0][nump[2]])
                else:
                    ts = names[1][nump[1]]
            if nump[0] != '0':
                ts = xconcat(names[0][str(nump[0])], 'hundred', ts)
            if int(nump) != 0:
                ts = xconcat(ts, place_value)
            s = xconcat(ts , s)
        elif l == 2: #10, 11, ... 99
            if int(nump) > 0 and int(nump) < 20:
                ts = names[0][nump]
            elif int(nump) > 19 and int(nump) < 100:
                if nump[1] != '0':
                    ts = xconcat(names[1][nump[0]], names[0][nump[1]])
                else:
                    ts = names[1][nump[0]]
            if int(nump) != 0:
                ts = xconcat(ts, place_value)
            s = xconcat(ts , s)
        elif l == 1:
            #if nump[0] != '0':
            ts =  names[0][str(nump[0])]
            if int(nump) != 0:
                ts = xconcat(ts, place_value)
            s = xconcat(ts , s)
        place_value_idx += 1
        nump = num[-3:]
        num = num[:-3]
    return s

def to_comma_placed(num):
    """Converts a number to string with comma placed at correct place values.
       e.g. 1123 to 1,123
       :attr num - an integer
    """
    assert type(num) == int, "must provide only integer as an argument"
    assert num >= 0, "number must be non-negative"
    num_str = str(num)
    assert len(num_str) < 121, "number must be less than or at max 0.9 x 10 ^ 121"
    index = 1
    new_str = ''
    l = len(num_str)
    for char in reversed(num_str):
        if index % 3 == 0 and l != index:
            new_str += char + ','
        else:
            new_str += char
        index += 1
    return new_str[::-1]

if __name__ == "__main__":
    no_list = [ 0, 1000, 1000000, 10000, 1012, 101, 112, 121, 110, 99, 999, 120,
                777, 88, 5000000, 70023,
                1230001]
    for no in no_list:
        print "%s => %s => %s" % (no, to_comma_placed(no), to_number_name(no)) 
