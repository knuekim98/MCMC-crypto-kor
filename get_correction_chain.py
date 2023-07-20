import random
from const import data_folder, book_name, FL, F, L, M, E
from jamo import h2j, j2hcj

with open(f'./{data_folder}/{book_name}', 'r', encoding='UTF8') as f:
    book = f.read()

book = book.replace('\u3000', ' ')
book = book.replace('―', '-')
book = book.replace('\n', '')
for _ in range(10): book = book.replace('  ', ' ')
book = j2hcj(h2j(book))

for i in FL: book = book.replace(i, 'B')
for i in F: book = book.replace(i, 'F')
for i in L: book = book.replace(i, 'L')
for i in M: book = book.replace(i, 'M')
for i in E: book = book.replace(i, 'E')
l = ['B', 'F', 'L', 'M', 'E']

cor = {'B':dict(), 'F':dict(), 'L':dict(), 'M':dict(), 'E':dict()}
for i in l:
    for j in l:
        cor[i][j] = book.count(i+j) / book.count(i)

with open(f'./{data_folder}/cor_chain', 'w', encoding='UTF8') as f:
    f.write(str(cor))
