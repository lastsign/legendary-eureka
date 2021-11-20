from tkinter import *
from tkinter import messagebox


alpha = '0123456789'


def gcdex(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = gcdex(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def del_fields(fields):
    for fil in fields:
        fil.config(state='normal')
        fil.delete(1.0, END)


def dis_fields(fields):
    for fil in fields:
        fil.config(state='disabled')


def cipher(a_, x_, n_):
    c = 1
    del_fields([c_text])
    a = int(a_)
    n = int(n_)
    x = int(x_)
    if x < 0:
        x = -x
        D, X, Y = gcdex(a, n)
        if D != 1:
            messagebox.showerror('Проверка нода', 'Решения нет')
        else:
            a = (X % n + n) % n
            while x:
                if x % 2 == 1:
                    c = (c * a) % n
                x //= 2
                a = (a * a) % n
            c_text.insert(1.0, f'{c}')
    else:
        while x:
            if x % 2 == 1:
                c = (c * a) % n
            x //= 2
            a = (a * a) % n
        c_text.insert(1.0, f'{c}')
    dis_fields([c_text])
    root.update()


def get_fields():
    a = a_field.get()
    x = x_field.get()
    n = n_field.get()
    return a, x, n


def check_fields(a, x, n):
    if not a or not x or not n:
        messagebox.showerror('Ввод данных', 'Одно из полей пустое')
    elif a[0] == '-' and not bool(set(a[1:]).issubset(set(alpha))):
        messagebox.showerror('Проверка полей', 'Некоректные символы')
    elif a[0] != '-' and not bool(set(a).issubset(set(alpha))):
        messagebox.showerror('Проверка полей', 'Некоректные символы')
    elif not bool(set(n).issubset(set(alpha))):
        messagebox.showerror('Проверка полей', 'Некоректные символы')
    elif n[0] != '-' and int(n) == 0:
        messagebox.showerror('Проверка полей', 'Модуль не может быть равен нулю')
    elif x[0] == '-' and not bool(set(x[1:]).issubset(set(alpha))):
        messagebox.showerror('Проверка полей', 'a и n не взаимно простые числа')
    elif x[0] != '-' and not bool(set(x).issubset(set(alpha))):
        messagebox.showerror('Проверка полей', 'Некоректные символы')
    else:
        return True
    return False


def cipher_text():
    a, x, n = get_fields()
    if check_fields(a, x, n):
        cipher(a, x, n)


root = Tk()

root['bg'] = '#ffb700'
root.title('POW by modulo')
root.geometry('600x500')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=0.25)

frame_mid = Frame(root, bg='#ffb700', bd=5)
frame_mid.place(relx=0, rely=0.4, relwidth=1, relheight=0.8)

a_label = Label(text='a', bg='#ffb700', font=40)
x_label = Label(text='x', bg='#ffb700', font=40)
n_label = Label(text='n', bg='#ffb700', font=40)
a_label.place(relx=0.2, rely=0.16)
x_label.place(relx=0.2, rely=0.22)
n_label.place(relx=0.2, rely=0.28)

a_field = Entry(frame_top, bg='white', font=30)
a_field.pack()

x_field = Entry(frame_top, bg='white', font=30)
x_field.pack()

n_field = Entry(frame_top, bg='white', font=30)
n_field.pack()


btn = Button(frame_top, text='Вычислить', command=cipher_text)
btn.pack()

с_label = Label(frame_mid, text='с', bg='#ffb700', font=40)
с_label.pack()
c_text = Text(frame_mid, height=1, borderwidth=0)
c_text.pack()

root.mainloop()