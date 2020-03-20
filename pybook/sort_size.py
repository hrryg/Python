def size(item):
    sizelist = ["XS","S","M","L"]
    pos = sizelist.index(item)
    return pos
data = ["S","M","XS","L","M","M","XS","S","M","L","M"]
data.sort(key=size)
print(data)
