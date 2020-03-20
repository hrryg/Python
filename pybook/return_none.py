def calc(num):
    unit_price = 180
    if not num.isdigit():
        return None
    price = int(num) * unit_price
    return price

while True:
    num = input("個数を入れてください。(qで終了)")
    if num == "":
        continue
    elif num == "q":
        break
    result = calc(num)
    print(result)
