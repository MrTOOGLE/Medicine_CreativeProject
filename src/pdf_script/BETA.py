from string import ascii_lowercase

s = ""
result = 0
for i in ascii_lowercase:
    if f'({i})' in s:
        result += 1
print(result)
