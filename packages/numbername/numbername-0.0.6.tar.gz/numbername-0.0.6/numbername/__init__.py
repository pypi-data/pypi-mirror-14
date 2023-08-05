# -*- coding: utf-8 -*-

"""numbername: Works on integers and longs to give human readble number forms.

Converts non-negative integer and long numbers to human
understandable number name, can also be used to form a comma placed numberic
string as per place value.

Example:

integer/long to number name conversion
 1123 -> one thousand one hundred twenty three

integer/long to comma placed string

 1123 -> 1,123
"""

from .src import to_number_name, to_comma_placed
