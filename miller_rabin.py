import numpy as np
from tkinter import *
from tkinter import messagebox
import random as rnd
import math

digits = '0123456789'


def del_fields(fields):
    for fil in fields:
        fil.config(state='normal')
        fil.delete(1.0, END)


def dis_fields(fields):
    for fil in fields:
        fil.config(state='disabled')


def get_fields():
    text = number.get()
    length = bit.get()
    return text, length


def check_fields(text):
    if not text:
        messagebox.showerror('Ввод данных', 'Поле для числа пустое')
    elif not bool(set(text).issubset(set(digits))):
        messagebox.showerror('Ввод данных', 'Некоректные символы для числа')
    else:
        return True
    return False


def pow_by_mod(a, t, n):
    x = 1
    while t:
        if t % 2 == 1:
            x = (x * a) % n
        t //= 2
        a = (a * a) % n
    return x


def test_miller_rabin(t, n):
    a = 2 + rnd.randint(1, n - 4)
    x = pow_by_mod(a, t, n)
    if x == 1 or x == n - 1:
        return True
    while t != n - 1:
        x = (x * x) % n
        t *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def is_prime_by_test_miller_rabin(n):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    t = n - 1
    while t % 2 == 0:
        t //= 2
    k = round(math.log2(n))
    for _ in range(k):
        if not test_miller_rabin(t, n):
            return False
    return True


def test_miller(n):
    u = nmo = n - 1
    s = 0
    while 2 ** s * u != nmo or u % 2 == 0:
        u //= 2
        s += 1
    if math.sqrt(n).is_integer():
        return 1
    for _ in range(round(math.log2(n))):
        a = rnd.randrange(2, n)
        if GCD(a, n) != 1:
            return 1
        b = pow_by_mod(a, u, n)
        if b != 1 and b != -1:
            x = b
            i = 0
            while i < s:
                i += 1
                x = (x * x) % n
                t_x = x % n
                while t_x >= 0:
                    t_x -= n
                if t_x % n == -1:
                    break
            if i == s:
                return 1
    return 0


def is_prime_by_test_fermat(n):
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True
    else:
        k = round(math.log2(n))
        for i in range(k):
            a = rnd.randint(2, n - 2)
            if pow_by_mod(a, n - 1, n) != 1:
                return False
    return True


def GCD(a, b):
    while b:
        a, b = b, a % b
    return a


def jacobi(a, b):
    if GCD(a, b) != 1:
        return 0
    r = 1
    if a < 0:
        a = -a
        if b % 4 == 3:
            r = -r
    if a == 1:
        return r
    while a:
        if a < 0:
            a = -a
            if b % 4 == 3:
                r = -r
        while a % 2 == 0:
            a //= 2
            if b % 8 == 3 or b % 8 == 5:
                r = -r
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            r = -r
        a = a % b
        if a > b // 2:
            a = a - b
    if b == 1:
        return r
    return 0


def is_prime_by_test_solovay_strassen(n):
    if n < 2:
        return False
    if n != 2 and n % 2 == 2:
        return False
    k = round(math.log2(n))
    for _ in range(k):
        a = rnd.randrange(n - 1) + 1
        if GCD(a, n) > 1:
            return False
        j = (n + jacobi(a, n)) % n
        r = pow_by_mod(a, (n - 1) // 2, n)
        if r != j or j == 0:
            return False
    return True


def select_test():
    del_fields([result])
    text, length = get_fields()
    if check_fields(text):
        if var.get() == 0:
            if is_prime_by_test_miller_rabin(int(text)):
                result.insert(1.0, f'Вероятно простое')
            else:
                result.insert(1.0, f'Составное')
        elif var.get() == 1:
            if is_prime_by_test_fermat(int(text)):
                result.insert(1.0, f'Вероятно простое')
            else:
                result.insert(1.0, f'Составное')
        elif var.get() == 2:
            if is_prime_by_test_solovay_strassen(int(text)):
                result.insert(1.0, f'Вероятно простое')
            else:
                result.insert(1.0, f'Составное')
    dis_fields([result])
    root.update()


def genetate_prime():
    del_fields([generate])
    text, length = get_fields()
    if check_fields(length):
        num = ''
        for _ in range(int(length)):
            num += f'{rnd.randrange(0, 2)}'
        num = int(num, 2)
        if num % 2 == 0:
            num += 1
        if var.get() == 0:
            r = is_prime_by_test_miller_rabin(num)
            while not r:
                num += 2
                r = is_prime_by_test_miller_rabin(num)
            if r:
                generate.insert(1.0, f'{num}')
            else:
                generate.insert(1.0, f'Не удалость найти, вероятно простое, число')
        elif var.get() == 1:
            r = is_prime_by_test_fermat(num)
            while not r:
                num += 2
                r = is_prime_by_test_fermat(num)
            if r:
                generate.insert(1.0, f'{num}')
            else:
                generate.insert(1.0, f'Не удалость найти, вероятно простое, число')
        elif var.get() == 2:
            r = is_prime_by_test_solovay_strassen(num)
            while not r:
                num += 2
                r = is_prime_by_test_solovay_strassen(num)
            if r:
                generate.insert(1.0, f'{num}')
            else:
                generate.insert(1.0, f'Не удалость найти, вероятно простое, число')
    dis_fields([generate])
    root.update()


root = Tk()
root['bg'] = '#ffb700'
root.title('Tests')
root.geometry('800x400')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=1)

number_label = Label(frame_top, text='Введите число', bg='#ffb700', font=40)
number_label.pack()

var = IntVar()
var.set(0)
miller_rabin = Radiobutton(text='Miller Rabin',
                           variable=var, value=0, bg='#ffb700')
fermat = Radiobutton(text='Fermat',
                     variable=var, value=1, bg='#ffb700')
solovay_strassen = Radiobutton(text='Solovay Strassen',
                               variable=var, value=2, bg='#ffb700')
button = Button(frame_top, text='Проверить',
                command=select_test)
miller_rabin.grid(row=0, column=0, ipadx=10, ipady=6, padx=100, pady=10)
fermat.grid(row=0, column=1, ipadx=10, ipady=6, padx=50, pady=10)
solovay_strassen.grid(row=0, column=2, ipadx=10, ipady=6, padx=100, pady=10)

number = Entry(frame_top, bg='white', font=30)
number.pack()
button.pack()

result_label = Label(frame_top, text='Результат проверки', bg='#ffb700', font=40)
result_label.pack()

result = Text(frame_top, height=1, borderwidth=0)
result.pack()

bit_label = Label(frame_top, text='Введите количество бит простого числа', bg='#ffb700', font=40)
bit_label.pack()

bit = Entry(frame_top, bg='white', font=30)
bit.pack()
btn = Button(frame_top, text='Сгенерировать', command=genetate_prime)
btn.pack()

generate_label = Label(frame_top, text='Сгенерированное число', bg='#ffb700', font=40)
generate_label.pack()

generate = Text(frame_top, height=1, borderwidth=0)
generate.pack()

root.mainloop()
