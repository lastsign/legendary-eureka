from tkinter import *
from tkinter import messagebox

alpha_rus = '0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alpha_eng = '0123456789abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'


def cipher(text, k, alpha, cip_text, c=1):
    ciphered = []
    K = int(k)
    ind_val = {i: alpha[i] for i in range(len(alpha))}
    val_ind = {alpha[i]: i for i in range(len(alpha))}
    for x in text:
        if x != ' ':
            ciphered.append(ind_val[(val_ind[x] + c * K) % len(alpha)])
        else:
            ciphered.append(x)
    cip_text.config(state='normal')
    cip_text.delete(1.0, END)
    cip_text.insert(1.0, ''.join(ciphered))
    cip_text.config(state='disabled')
    root.update()


def get_fields():
    text = text_field.get()
    k = k_field.get()
    v0 = var0.get()
    v1 = var1.get()
    return text, k, v0, v1


def check_fields(text, k, v0, v1):
    if v1 == '0' and v0 == '0':
        messagebox.showerror('Выбор языка словоря', 'Выберете один из языков алфавита')
    elif v1 != '0' and v0 != '0':
        messagebox.showerror('Выбор языка словоря', 'Нужно выбрать только один язык для алфовита')
    elif not k or not text:
        messagebox.showerror('Ввод данных', 'Одно или два поля пустые')
    elif k[0] == '-' and not bool(set(k[1:]).issubset(set(digits))):
        messagebox.showerror('Проверка k', 'Некорректные символы для k')
    elif k[0] != '-' and not bool(set(k).issubset(set(digits))):
        messagebox.showerror('Проверка k', 'Некорректные символы для k')
    elif k == '0':
        messagebox.showerror('Проверка k', 'k не может быть равно 0')
    elif v0 == 'ru' and not bool(set(text).issubset(set(alpha_rus + ' '))):
        messagebox.showerror('Проверка слова', 'Некоректные символы для русского алфавита')
    elif v1 == 'eng' and not bool(set(text).issubset(set(alpha_eng + ' '))):
        messagebox.showerror('Проверка слова', 'Некоректные символы для английского алфавита')
    else:
        return True
    return False


def cipher_text():
    text, k, v0, v1 = get_fields()
    if cipher_label['text'] != '':
        messagebox.showerror('Проверка этапа шифрования', 'Текст уже был зашифрован')
    elif check_fields(text, k, v0, v1):
        cipher_label['text'] = 'Криптограмма'
        decipher_label['text'] = ''
        if v1 == 'eng':
            cipher(text, k, alpha_eng, cipher_text)
            decipher_text.delete(1.0, END)
        elif v0 == 'ru':
            cipher(text, k, alpha_rus, cipher_text)
            decipher_text.delete(1.0, END)


def decipher_text():
    text, k, v0, v1 = get_fields()
    if cipher_label['text'] == '':
        messagebox.showerror('Проверка этапа шифрования', 'Сначала нужно зашифровать текст')
    elif len(text) != len(cipher_text.get(1.0, 'end-1c')):
        messagebox.showerror('Проверка этапа шифрования', 'Зашифрованный текст был изменен')
    elif check_fields(text, k, v0, v1):
        cipher_label['text'] = ''
        decipher_label['text'] = 'Расшифрованный текст'
        if v1 == 'eng':
            cipher(cipher_text.get(1.0, 'end-1c'), k, alpha_eng, decipher_text, c=-1)
            cipher_text.delete(1.0, END)
        elif v0 == 'ru':
            cipher(cipher_text.get(1.0, 'end-1c'), k, alpha_rus, decipher_text, c=-1)
            cipher_text.delete(1.0, END)


def focus_text(event):
   cipher_text.config(state='normal')
   cipher_text.focus()
   cipher_text.config(state='disabled')


root = Tk()

root['bg'] = '#ffb700'
root.title('Caesar cipher')
root.geometry('600x400')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=0.25)

frame_mid = Frame(root, bg='#ffb700', bd=5)
frame_mid.place(relx=0, rely=0.45, relwidth=1, relheight=0.2)

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0, rely=0.7, relwidth=1, relheight=0.2)

var0 = StringVar()
var1 = StringVar()

ch0 = Checkbutton(frame_top, text='Рус', variable=var0, onvalue='ru')
ch1 = Checkbutton(frame_top, text='Eng', variable=var1, onvalue='eng')

ch0.place(relx=0.68, rely=0)
ch1.place(relx=0.68, rely=0.3)

ch0.deselect()
ch1.deselect()

text_label = Label(text='Введите исх. текст:')
k_label = Label(text='Введите k:')

text_label.place(relx=0.11, rely=0.17)
k_label.place(relx=0.11, rely=0.24)

text_field = Entry(frame_top, bg='white', font=30)
text_field.pack()

k_field = Entry(frame_top, bg='white', font=30)
k_field.pack()

btn = Button(frame_top, text='Зашифровать текст', command=cipher_text)
btn.pack()

btn = Button(frame_mid, text='Расшифровать текст', command=decipher_text)
btn.place(relx=0.355, rely=0.5)

cipher_label = Label(frame_mid, text='', bg='#ffb700', font=40)
cipher_label.pack()

decipher_label = Label(frame_bottom, text='', bg='#ffb700', font=40)
decipher_label.pack()

cipher_text = Text(frame_mid, height=1, borderwidth=0)
cipher_text.pack()
decipher_text = Text(frame_bottom, height=1, borderwidth=0)
decipher_text.pack()
cipher_text.configure(state='disable')
cipher_text.bind('<Button-1>', focus_text)

root.mainloop()