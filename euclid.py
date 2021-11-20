from tkinter import *
from tkinter import messagebox

alpha = '0123456789'


def del_fields(fields):
    for fil in fields:
        fil.config(state='normal')
        fil.delete(1.0, END)


def dis_fields(fields):
    for fil in fields:
        fil.config(state='disabled')


def cipher(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = cipher(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def get_fields():
    a = a_field.get()
    b = b_field.get()
    return a, b


def check_fields(a, b):
    if not a or not b:
        messagebox.showerror('Ввод данных', 'Одно из полей пустое')
    elif not bool(set(a).issubset(set(alpha))):
        messagebox.showerror('Проверка слова', 'Некоректные символы')
    elif not bool(set(b).issubset(set(alpha))):
        messagebox.showerror('Проверка ключа', 'Некоректные символы')
    else:
        return True
    return False


def cipher_text():
    a, b = get_fields()
    if check_fields(a, b):
        del_fields([x_text, y_text, d_text])
        a = int(a)
        b = int(b)
        d, x, y = cipher(a, b)
        x_text.insert(1.0, f'{x}')
        y_text.insert(1.0, f'{y}')
        d_text.insert(1.0, f'{d}')
        dis_fields([x_text, y_text, d_text])
        root.update()


root = Tk()

root['bg'] = '#ffb700'
root.title('Extended Euclidean Algorithm')
root.geometry('600x500')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=0.25)

frame_mid = Frame(root, bg='#ffb700', bd=5)
frame_mid.place(relx=0, rely=0.4, relwidth=1, relheight=0.8)

a_label = Label(text='A', bg='#ffb700', font=40)
b_label = Label(text='B', bg='#ffb700', font=40)
a_label.place(relx=0.2, rely=0.16)
b_label.place(relx=0.2, rely=0.22)

a_field = Entry(frame_top, bg='white', font=30)
a_field.pack()

b_field = Entry(frame_top, bg='white', font=30)
b_field.pack()


btn = Button(frame_top, text='Вычислить', command=cipher_text)
btn.pack()

x_label = Label(frame_mid, text='x', bg='#ffb700', font=40)
x_label.pack()
x_text = Text(frame_mid, height=1, borderwidth=0)
x_text.pack()

y_label = Label(frame_mid, text='y', bg='#ffb700', font=40)
y_label.pack()
y_text = Text(frame_mid, height=1, borderwidth=0)
y_text.pack()

d_label = Label(frame_mid, text='gcd', bg='#ffb700', font=40)
d_label.pack()
d_text = Text(frame_mid, height=1, borderwidth=0)
d_text.pack()


root.mainloop()