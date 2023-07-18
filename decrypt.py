import random
from const import data_folder, book_name
from math import log, exp


with open(f'./{data_folder}/chain', 'r', encoding='UTF8') as f:
    chain = eval(f.read())

with open(f'./{data_folder}/ciphertext', 'r', encoding='UTF8') as f:
    c = f.read()

freq = dict()


def get_dec(df):
    dec = ''
    for i in c:
        dec += df[i]
    return dec


def get_possibility(dec):
    v = log(freq[dec[0]])
    for i in range(len(c)-1):
        v += log(chain[dec[i]][dec[i+1]] + exp(-25))
    
    return v


c1 = list(set(c))
c1.sort()

with open(f'./{data_folder}/{book_name}', 'r', encoding='UTF8') as f:
    book = f.read()

book = book.replace('\n', '').lower()
book = book.replace('à', 'a')
book = book.replace('ä', 'a')
book = book.replace('é', 'e')
book = book.replace('ê', 'e')

x = list(set(book))
x.sort()
for i in x:
    freq[i] = book.count(i)/len(book)

x.sort(key=lambda i : freq[i])
x.reverse()
x = x[:len(c1)]


random.shuffle(x)

df = dict()
for i in range(len(c1)):
    df[c1[i]] = x[i]

dec = get_dec(df)
pos = get_possibility(dec)

print(df)
print(pos)


jump = 0
for k in range(50000):
    r1 = random.randrange(0, len(c1))
    r2 = r1
    while r2 == r1: r2 = random.randrange(0, len(c1))

    pos = get_possibility(get_dec(df))
    new_df = df.copy()
    new_df[c1[r2]] = df[c1[r1]]
    new_df[c1[r1]] = df[c1[r2]]
    new_pos = get_possibility(get_dec(new_df))

    if new_pos > pos: 
        pos = new_pos
        df = new_df
    elif new_pos - pos > log(random.random()): 
        pos = new_pos
        df = new_df
        jump += 1

print(df)
print(pos)
print(jump)

print(get_dec(df))
