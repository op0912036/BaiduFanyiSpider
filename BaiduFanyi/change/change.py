import os

# list = []
with open('./change.txt', 'r') as file:
    list = file.readlines()

print()

list3 = []
for i in list:
    list2 = []
    w = i.partition(':')

    w1 = w[0]
    w2 = w[2].lstrip()
    w2 = w2.rstrip(os.linesep)
    wl = '"' + w1 + '"'
    wr = '"' + w2 + '",'

    list2.append(wl)
    list2.append(wr)


    ret = ":".join(list2)
    print(ret)
