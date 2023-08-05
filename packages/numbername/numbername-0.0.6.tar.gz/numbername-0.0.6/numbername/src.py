# -*- coding: utf-8 -*-

"""contains the code for numbername package.
"""


def to_number_name(num):
    """Converts a number to a number name.
       e.g. 1123 to one thousand one hundred twenty three
       :param num - an integer
       :return: string representing the number name
    """

    def xconcat(*strs):
        """concatenate all the input strings using spaces
        :param strs: strings
        :return: concatenation of all string
        """
        seperator = ' '
        result = ''
        for string in strs:
            if string.strip() != '':
                if result.strip() != '':
                    result += seperator + string
                else:
                    result = string
        return result

    assert isinstance(num, int) or isinstance(num, long), "must provide only int or " \
        "long as an argument"
    assert num >= 0, "number must be non negative"
    assert num <= 10 ** 64, "number must be less than or at max 0.9 x 10 ^ 65"
    num = str(num)
    names = [
        {
            "0":"zero",
            "1":"one",
            "2":"two",
            "3":"three",
            "4":"four",
            "5":"five",
            "6":"six",
            "7":"seven",
            "8":"eight",
            "9":"nine",
            "10":"ten",
            "11":"eleven",
            "12":"twelve",
            "13":"thirteen",
            "14":"fourteen",
            "15":"fifteen",
            "16":"sixteen",
            "17":"seventeen",
            "18":"eighteen",
            "19":"nineteen"},
        {
            "2":"twenty",
            "3":"thirty",
            "4":"forty",
            "5":"fifty",
            "6":"sixty",
            "7":"seventy",
            "8":"eighty",
            "9":"ninety"},
        [
            "", "thousand", "million", "billion", "trillion", "quadrillion",
            "quintillion", "sextillion", "septillion", "octillion",
            "nonillion", "decillion", "undecillion", "duodecillion",
            "tredecillion", "quattuordecillion", "quindecillion",
            "sexdecillion", "septdecillion", "octdecillion",
            "novemdecillion", "vigintillion"]
    ]

    place_value_idx = 0
    nump = num[-3:]
    num = num[:-3]

    result = ''
    while len(nump) > 0:
        place_value = names[2][place_value_idx]
        length = len(nump)
        temp_string = ''
        if length == 3:
            if int(nump[-2:]) > 0 and int(nump[-2:]) < 20:
                temp_string = names[0][str(int(nump[-2:]))]
            elif int(nump[-2:]) > 19 and int(nump[-2:]) < 100:
                if nump[2] != '0':
                    temp_string = xconcat(names[1][nump[1]], names[0][nump[2]])
                else:
                    temp_string = names[1][nump[1]]
            if nump[0] != '0':
                temp_string = xconcat(names[0][str(nump[0])], 'hundred', temp_string)
            if int(nump) != 0:
                temp_string = xconcat(temp_string, place_value)
            result = xconcat(temp_string, result)
        elif length == 2: # 10, 11, ... 99
            if int(nump) > 0 and int(nump) < 20:
                temp_string = names[0][nump]
            elif int(nump) > 19 and int(nump) < 100:
                if nump[1] != '0':
                    temp_string = xconcat(names[1][nump[0]], names[0][nump[1]])
                else:
                    temp_string = names[1][nump[0]]
            if int(nump) != 0:
                temp_string = xconcat(temp_string, place_value)
            result = xconcat(temp_string, result)
        elif length == 1:
            temp_string = names[0][str(nump[0])]
            if int(nump) != 0:
                temp_string = xconcat(temp_string, place_value)
            result = xconcat(temp_string, result)
        place_value_idx += 1
        nump = num[-3:]
        num = num[:-3]
    return result


def to_comma_placed(num):
    """Converts a number to string with comma placed at correct place values.
       e.g. 1123 to 1,123
       :attr num - an integer
    """

    assert isinstance(num, int) or isinstance(num, long), "must provide only int or " \
        "long as an argument"
    assert num >= 0, "number must be non-negative"
    assert num <= 10 ** 64, "number must be less than or at max 0.1 x 10 ^ 65"
    num_str = str(num)
    index = 1
    new_str = ''
    length = len(num_str)
    for char in reversed(num_str):
        if index % 3 == 0 and length != index:
            new_str += char + ','
        else:
            new_str += char
        index += 1
    return new_str[::-1]

if __name__ == "__main__":
    pass
