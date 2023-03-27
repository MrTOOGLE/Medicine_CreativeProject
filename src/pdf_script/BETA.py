import re


txt = "1 2 34"
print(re.search(r"\d{2}", txt).group())