from const import data_folder, book_name, language
from jamo import h2j, j2hcj


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

print(x)

c = dict()
for i in x: c[i] = dict()
for i in x:
    for j in x:
        c[i][j] = book.count(i+j) / book.count(i)

with open(f'./{data_folder}/chain', 'w', encoding='UTF8') as f:
    f.write(str(c))