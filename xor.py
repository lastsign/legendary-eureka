from tkinter import *
from tkinter import messagebox
import random
import numpy as np

alpha_rus = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def del_fields(fields):
    for fil in fields:
        fil.config(state='normal')
        fil.delete(1.0, END)


def dis_fields(fields):
    for fil in fields:
        fil.config(state='disabled')


def cipher(text, k, cip_text):
    ciphered = []
    del_fields([bin_text, bin_k, bincipher_text, cip_text])
    ind_val = {f'{i:05b}': v for i, v in enumerate(alpha_rus)}
    val_ind = {v: f'{i:05b}' for i, v in enumerate(alpha_rus)}
    for i, x in enumerate(text):
        if x != ' ':
            bins = ''
            for bs, bk in zip(val_ind[x], val_ind[k[i % len(k)]]):
                bins += f'{int(bs) ^ int(bk)}'
            bin_text.insert(END, val_ind[x])
            bincipher_text.insert(END, bins)
            ciphered.append(ind_val[bins])
        else:
            bin_text.insert(END, x)
            ciphered.append(x)
            bincipher_text.insert(END, x)
    for let in k:
        k_field.insert(END, let)
        bin_k.insert(END, val_ind[let])
    ch0.deselect()
    cip_text.insert(1.0, ''.join(ciphered))
    dis_fields([bin_text, bin_k, bincipher_text, cip_text])
    root.update()


def get_fields():
    text = text_field.get()
    k = k_field.get(1.0, 'end-1c')
    v0 = var0.get()
    return text, k, v0


def check_fields(text, k, v0):
    if not text:
        messagebox.showerror('Ввод данных', 'Поле для текста пустое')
    elif k and v0 == 0:
        messagebox.showerror('Ввод данных', 'Нужно либо ввести ключ, либо выбрать генерацию ключа')
    elif not bool(set(text).issubset(set(alpha_rus + ' '))):
        messagebox.showerror('Проверка слова', 'Некоректные символы для алфавита')
    elif not bool(set(k).issubset(set(alpha_rus + ' '))):
        messagebox.showerror('Проверка ключа', 'Некоректные символы для алфавита')
    else:
        return True
    return False


def gen_k(n):
    lst = []
    one = np.ones(n // 2, dtype='int')
    zer = np.zeros(n - n // 2, dtype='int')
    k = np.concatenate([one, zer], axis=None)
    random.shuffle(k)
    k = ''.join(str(e) for e in k)
    ind_val = {f'{i:05b}': v for i, v in enumerate(alpha_rus)}
    for i in range(0, len(k), 5):
        lst.append(ind_val[k[i:i + 5]])
    return lst


def cipher_text():
    text, k, v0 = get_fields()
    if cipher_label['text'] != '':
        messagebox.showerror('Проверка этапа шифрования', 'Текст уже был зашифрован')
    elif check_fields(text, k, v0):
        cipher_label['text'] = 'Криптограмма'
        decipher_label['text'] = ''
        if v0 == 'gen':
            k = gen_k(len(text) * 5)
        cipher(text, k, text_cipher)
        text_decipher.delete(1.0, END)


def decipher(text, k, cip_text):
    ciphered = []
    del_fields([bin_text_decipher, cip_text])
    bin_text_decipher.delete(1.0, END)
    ind_val = {f'{i:05b}': v for i, v in enumerate(alpha_rus)}
    val_ind = {v: f'{i:05b}' for i, v in enumerate(alpha_rus)}
    for i, x in enumerate(text):
        if x != ' ':
            bins = ''
            for bs, bk in zip(val_ind[x], val_ind[k[i % len(k)]]):
                bins += f'{int(bs) ^ int(bk)}'
            bin_text_decipher.insert(END, bins)
            ciphered.append(ind_val[bins])
        else:
            ciphered.append(x)
            bin_text_decipher.insert(END, x)
    cip_text.insert(1.0, ''.join(ciphered))
    dis_fields([bin_text_decipher, cip_text])
    root.update()


def decipher_text():
    text, k, v0 = get_fields()
    if cipher_label['text'] == '':
        messagebox.showerror('Проверка этапа шифрования', 'Сначала нужно зашифровать текст')
    elif check_fields(text_cipher.get(1.0, 'end-1c'), k, v0):
        cipher_label['text'] = ''
        decipher_label['text'] = 'Расшифрованный текст'
        decipher(text_cipher.get(1.0, 'end-1c'), k, text_decipher)
        text_cipher.delete(1.0, END)


def focus_text(event):
    text_cipher.config(state='normal')
    text_cipher.focus()
    text_cipher.config(state='disabled')


root = Tk()

root['bg'] = '#ffb700'
root.title('XOR cipher')
root.geometry('1200x700')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=0.25)

frame_mid = Frame(root, bg='#ffb700', bd=5)
frame_mid.place(relx=0, rely=0.4, relwidth=1, relheight=0.8)

var0 = StringVar()

ch0 = Checkbutton(frame_top, text='Generate', variable=var0, onvalue='gen')

ch0.place(relx=0.68, rely=0.3)

ch0.deselect()

text_label = Label(text='Введите исх. текст:', bg='#ffb700', font=40)
k_label = Label(text='Введите k:', bg='#ffb700', font=40)

text_label.place(relx=0.11, rely=0.16)
k_label.place(relx=0.11, rely=0.22)

text_field = Entry(frame_top, bg='white', font=30)
text_field.pack()

k_field = Text(frame_top, height=1, width=26, borderwidth=0)
k_field.pack()

btn = Button(frame_top, text='Зашифровать текст', command=cipher_text)
btn.pack()

bintext_label = Label(frame_mid, text='Бинарный код исходного текста', bg='#ffb700', font=40)
bintext_label.pack()
bin_text = Text(frame_mid, height=1, borderwidth=0)
bin_text.pack()
bink_label = Label(frame_mid, text='Бинарный код ключа', bg='#ffb700', font=40)
bink_label.pack()
bin_k = Text(frame_mid, height=1, borderwidth=0)
bin_k.pack()
bincipher_label = Label(frame_mid, text='Банарная криптограмма', bg='#ffb700', font=40)
bincipher_label.pack()
bincipher_text = Text(frame_mid, height=1, borderwidth=0)
bincipher_text.pack()
cipher_label = Label(frame_mid, text='', bg='#ffb700', font=40)
cipher_label.pack()
text_cipher = Text(frame_mid, height=1, borderwidth=0)
text_cipher.pack()

btn = Button(frame_mid, text='Расшифровать текст', command=decipher_text)
btn.pack()
bintext_decipher = Label(frame_mid, text='Расшифрованый бинарный код', bg='#ffb700', font=40)
bintext_decipher.pack()
bin_text_decipher = Text(frame_mid, height=1, borderwidth=0)
bin_text_decipher.pack()
decipher_label = Label(frame_mid, text='', bg='#ffb700', font=40)
decipher_label.pack()
text_decipher = Text(frame_mid, height=1, borderwidth=0)
text_decipher.pack()

bin_text.configure(state='disable')
bin_text.bind('<Button-1>', focus_text)
bin_k.configure(state='disable')
bin_k.bind('<Button-1>', focus_text)
bincipher_text.configure(state='disable')
bincipher_text.bind('<Button-1>', focus_text)
bin_text_decipher.configure(state='disable')
bin_text_decipher.bind('<Button-1>', focus_text)
text_decipher.configure(state='disable')
text_decipher.bind('<Button-1>', focus_text)
text_cipher.configure(state='disable')
text_cipher.bind('<Button-1>', focus_text)

root.mainloop()
