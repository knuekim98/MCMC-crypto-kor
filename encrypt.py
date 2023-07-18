import random
from const import data_folder, language
from jamo import h2j, j2hcj


with open(f'./{data_folder}/plaintext', 'r', encoding='UTF8') as f:
    p = f.read()

p.replace('\n', '')

if language == 'eng':
    p = p.lower()
elif language == 'kor':
    p = j2hcj(h2j(p))

a1 = list(set(p))
a1.sort()
l = len(a1)
a2 = [chr(i) for i in range(65, 65+l)]
random.shuffle(a2)

d = dict()
for i in range(l):
    d[a1[i]] = a2[i]
print(d)

c = ''
for i in p:
    c += d[i]

with open(f'./{data_folder}/ciphertext', 'w') as f:
    f.write(c)