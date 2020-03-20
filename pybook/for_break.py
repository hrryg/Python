numlist = [3, 4.2, 10, "x", 1, 9]
sum = 0
for num in numlist:
    if not isinstance(num, (int,float)):
        print(num,"数値ではない")
        break
    sum += num
    print(num, "/", sum)
