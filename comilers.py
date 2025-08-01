from MyScanner import tokanize
from MyParser import parse

tokens ,lines = tokanize("test.txt")

with open("Scanner_output.txt", 'w+') as fw:
    for token in tokens:
        fw.write(str(token) + "\n")
l = parse(lines)
with open("tockenTypes.txt", "w+")as fw:
    for line in lines :
        fw.write(str(line) + "\n")

with open("Parser_output.txt", "w+")as fw:
    for line in l :
        fw.write(str(line) + "\n")


