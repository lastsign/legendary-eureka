import random

alpha = 'ЕЖЗИЙК'
val = ['11000101', '11000110', '11000111', '11001000', '11001001', '11001010']

dlv = {k: v for k, v in zip(alpha, val)}
dvl = {v: k for k, v in zip(alpha, val)}

info = [2, 4, 5, 6, 8, 9, 10, 11]
cont = [0, 1, 3, 7]
odd = [12]
c0 = [2, 4, 6, 8, 10]
c1 = [2, 5, 6, 9, 10]
c3 = [4, 5, 6, 11]
c7 = [8, 9, 10, 11]
dcont = {k: v for k, v in zip(cont, [c0, c1, c3, c7])}
letter = alpha[random.randint(0, 5)]
print(f'Была выбрана переменная:\n{letter}')
lst = [0] * 13
bit = dlv[letter]


def conferm(bits):
    for inds in cont:
        summ = 0
        for i in dcont[inds]:
            summ ^= bits[i]
        bits[inds] = summ
    return bits


def conferm_odd(bits, odd):
    summ = 0
    for v in info + cont:
        summ ^= bits[v]
    bits[odd] = summ
    return bits


def print_bits(bits, str=''):
    print(f'Проверочные биты и биты символа {letter}{str}:')
    for i, v in enumerate(bits):
        if i not in info:
            print(v, end='')
        else:
            print('_', end='')
    print()
    for i, v in enumerate(bits):
        if i in info:
            print(v, end='')
        else:
            print('_', end='')
    print()


for i, v in enumerate(info):
    lst[v] = int(bit[i])

lst = conferm(lst)
lst = conferm_odd(lst, odd[0])

print_bits(lst)

wrnglst = lst.copy()

rndind = random.randint(0, 7)
print(f'Сделаем ошибку в одном бите: {info[rndind]}')
wrnglst[info[rndind]] = 0 if wrnglst[info[rndind]] == 1 else 1

oldwrnglst = wrnglst.copy()
print_bits(oldwrnglst, str=' с ошибкой, до пересчета')
wrnglst = conferm(wrnglst)

diff = []
for i in range(len(lst)):
    if oldwrnglst[i] != wrnglst[i]:
        diff.append(i + 1)

wrnglst = conferm_odd(wrnglst, odd[0])
print_bits(wrnglst, str=' с ошибкой, после пересчета')
wrnglst[sum(diff) - 1] = 0 if wrnglst[sum(diff) - 1] == 1 else 1
st = []
for i in info:
    st.append(wrnglst[i])
dec_letter = dvl[''.join([str(i) for i in st])]
print(f'Декодированный символ:\n{dec_letter}\n------------------------------------')

rndind2 = rndind1 = random.randint(0, 7)
while rndind2 == rndind1:
    rndind2 = random.randint(0, 7)
print(f'Сделаем ошибку в двух битах: {info[rndind1]}, {info[rndind2]}')
wrnglst[info[rndind1]] = 0 if wrnglst[info[rndind1]] == 1 else 1
wrnglst[info[rndind2]] = 0 if wrnglst[info[rndind2]] == 1 else 1


oldwrnglst = wrnglst.copy()
print_bits(oldwrnglst, str=' с ошибкой, до пересчета')
wrnglst = conferm(wrnglst)

diff = []
for i in range(len(lst)):
    if oldwrnglst[i] != wrnglst[i]:
        diff.append(i + 1)

wrnglst = conferm_odd(wrnglst, odd[0])
print_bits(wrnglst, str=' с ошибкой, после пересчета')
if diff:
    print(f'{diff}Лист с индексами в которых отличается код не пуст, поэтому есть ошибка, но мы не можем ее исправить, потому что\n'
          'может быть случай когда сумма индексов с ошибкой выйдет за пределы нашего битного представления символа')
