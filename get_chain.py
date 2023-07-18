from const import data_folder, book_name


with open(f'./{data_folder}/{book_name}', 'r', encoding='UTF8') as f:
    book = f.read()

book = book.replace('\n', '').lower()
book = book.replace('à', 'a')
book = book.replace('ä', 'a')
book = book.replace('é', 'e')
book = book.replace('ê', 'e')
x = list(set(book))
x.sort()

c = dict()
for i in x: c[i] = dict()
for i in x:
    for j in x:
        c[i][j] = book.count(i+j) / book.count(i)

with open(f'./{data_folder}/chain', 'w') as f:
    f.write(str(c))