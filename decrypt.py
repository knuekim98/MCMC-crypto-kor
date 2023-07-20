import random
from const import data_folder, book_name, language, FL, F, L, M, E
from math import log, exp
from jamo import h2j, j2hcj
from hangul_utils import join_jamos
import matplotlib.pyplot as plt


with open(f'./{data_folder}/chain', 'r', encoding='UTF8') as f:
    chain = eval(f.read())

if language == 'kor':
    with open(f'./{data_folder}/cor_chain', 'r', encoding='UTF8') as f:
        cor_chain = eval(f.read())

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


def get_cor_possibility(dec):
    for i in FL: dec = dec.replace(i, 'B')
    for i in F: dec = dec.replace(i, 'F')
    for i in L: dec = dec.replace(i, 'L')
    for i in M: dec = dec.replace(i, 'M')
    for i in E: dec = dec.replace(i, 'E')

    v = 0
    for i in range(len(c)-1):
        v += log(cor_chain[dec[i]][dec[i+1]] + exp(-25))

    return v


def mcmc(x, c1, verbose=True, write=True):
    random.shuffle(x)

    df = dict()
    for i in range(len(c1)):
        df[c1[i]] = x[i]
    pos = get_possibility(get_dec(df))

    if verbose:
        print(df)
        print(pos)

    jump = 0
    pos_plot = []
    for k in range(20000):
        dec = get_dec(df)
        pos = get_possibility(dec)
        if language == 'kor': cor_pos = get_cor_possibility(dec)

        new_df = df.copy()
        r1 = random.randrange(0, len(c1))
        r2 = r1
        while r2 == r1: r2 = random.randrange(0, len(c1))

        new_df[c1[r2]] = df[c1[r1]]
        new_df[c1[r1]] = df[c1[r2]]
        new_dec = get_dec(new_df)
        new_pos = get_possibility(new_dec)
        if language == 'kor': new_cor_pos = get_cor_possibility(new_dec)

        if new_pos > pos: 
            pos = new_pos
            df = new_df
        elif language == 'kor':
            if new_pos - pos + new_cor_pos - cor_pos > log(random.random()): 
                pos = new_pos
                df = new_df
                jump += 1
        else:
            if new_pos - pos > log(random.random()): 
                pos = new_pos
                df = new_df
                jump += 1

        if k%400 == 0: 
            pos_plot.append(pos)

    if language == 'kor': result = join_jamos(get_dec(df))
    else: result = get_dec(df)
    print(result)

    if verbose:
        print(df)
        print(pos)
        print(jump)

    if write:
        with open(f'./{data_folder}/deciphertext', 'w', encoding='UTF8') as f:
            f.write(result)

    return pos_plot


c1 = list(set(c))
c1.sort()

with open(f'./{data_folder}/{book_name}', 'r', encoding='UTF8') as f:
    book = f.read()

if language == 'eng':
    book = book.replace('\n', '').lower()
    book = book.replace('à', 'a')
    book = book.replace('ä', 'a')
    book = book.replace('é', 'e')
    book = book.replace('ê', 'e')

if language == 'kor':
    book = book.replace('\u3000', ' ')
    book = book.replace('―', '-')
    book = book.replace('\n', '')
    for _ in range(10): book = book.replace('  ', ' ')
    book = j2hcj(h2j(book))

x = list(set(book))
x.sort()
for i in x:
    freq[i] = book.count(i)/len(book)

x.sort(key=lambda i : freq[i])
x.reverse()
x = x[:len(c1)]


loop = 30

avg_plot = [0]*50
result_plot = [0]*loop
for _ in range(loop):
    print(f'loop {_+1}/{loop}')
    pos_plot = mcmc(x, c1, True, False)
    result_plot[_] = pos_plot[-1]
    for i in range(50):
        avg_plot[i] += pos_plot[i]
    

plt.subplot(1, 2, 1)
plt.plot([i*400 for i in range(50)], [p/loop for p in avg_plot], '.-')
plt.xlabel('iterations')
plt.ylabel('log possibility')

plt.subplot(1, 2, 2)
plt.bar([i+1 for i in range(loop)], result_plot)
plt.xlabel('loop')
plt.ylabel('final log possibility')

plt.tight_layout()
plt.show()