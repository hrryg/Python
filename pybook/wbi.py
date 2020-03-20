from random import randint
miss = 0
correct = 0
print("問題！3回間違えたら終了。qで止める")
while miss<3:
    a = randint(1,100)
    b = randint(1,100)
    ans = a + b
    question = f"{a}+{b}は？"
    value = input(question)
    if value == "q":
        break
    if value == str(ans):
        correct += 1
        print("正解です！")
    else:
        miss += 1
        print("間違い！","x" * miss)
print("-"*20)
print("正解:",correct)
print("間違い:",miss)
