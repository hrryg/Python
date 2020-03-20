def num_gen():
    n = 0
    while True:
        num = n*n + 2*n + 3
        yield num
        n += 1

def do(sum):
    return (num%2,num%3)

gen = num_gen()
for i in range(1,10):
    num = next(gen)
    result = do(num)
    print(result)
