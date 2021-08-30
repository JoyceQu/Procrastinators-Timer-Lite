import random
f = open('record.txt', 'w')
for i in range(1000):
    y = 2021
    m = random.randint(1, 12)
    #m = 8
    d = random.randint(1, 28)
    t = random.randint(30, 500)
    c = random.randint(1, 6)
    f.write(str(y) + ' ' + str(m) + ' ' + str(d) + ' ' + str(c) + ' ' + str(t) + '\n')

f.close()