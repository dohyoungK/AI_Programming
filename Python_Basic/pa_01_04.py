'''201624419/KimDoHyoung/010-2399-0652'''

import re

string = input("Enter a string: ")
subString = input("Enter a subString: ")

count = len(re.findall(subString, string))

print("Number of non-overlapping occurrences:", count)