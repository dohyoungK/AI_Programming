'''201624419/KimDoHyoung'''

import re

string = input("Enter a string: ")
subString = input("Enter a subString: ")

count = len(re.findall(subString, string))

print("Number of non-overlapping occurrences:", count)
