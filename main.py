from tkinter import *
import random
import string
min_alpha_entry = None
max_alpha_entry = None
min_numeric_entry = None
max_numeric_entry = None
min_special_entry = None
max_special_entry = None
total_length_entry = None

# Createa functiei pentru interfata grafica


def create_gui():
    global min_alpha_entry, max_alpha_entry, min_numeric_entry, max_numeric_entry
    global min_special_entry, max_special_entry, total_length_entry, password_listbox

    # Crearea interfatei grafice
    root = Tk()
    root.title("Generator de Parole")
    root.geometry("330x500")

    # Crearea formularului
    min_alpha_label = Label(root, text="Numar minim de caractere alfabetice:")
    min_alpha_label.grid(row=1, column=0, padx=10, pady=5)
    min_alpha_entry = Entry(root, width=10)
    min_alpha_entry.grid(row=1, column=1, padx=10, pady=5)

    max_alpha_label = Label(root, text="Numar maxim de caractere alfabetice:")
    max_alpha_label.grid(row=2, column=0, padx=10, pady=5)
    max_alpha_entry = Entry(root, width=10)
    max_alpha_entry.grid(row=2, column=1, padx=10, pady=5)

    min_numeric_label = Label(root, text="Numar minim de caractere numerice:")
    min_numeric_label.grid(row=3, column=0, padx=10, pady=5)
    min_numeric_entry = Entry(root, width=10)
    min_numeric_entry.grid(row=3, column=1, padx=10, pady=5)

    max_numeric_label = Label(root, text="Numar maxim de caractere numerice:")
    max_numeric_label.grid(row=4, column=0, padx=10, pady=5)
    max_numeric_entry = Entry(root, width=10)
    max_numeric_entry.grid(row=4, column=1, padx=10, pady=5)

    min_special_label = Label(root, text="Numar minim de caractere speciale:")
    min_special_label.grid(row=5, column=0, padx=10, pady=5)
    min_special_entry = Entry(root, width=10)
    min_special_entry.grid(row=5, column=1, padx=10, pady=5)

    max_special_label = Label(root, text="Numar maxim de caractere speciale:")
    max_special_label.grid(row=6, column=0, padx=10, pady=5)
    max_special_entry = Entry(root, width=10)
    max_special_entry.grid(row=6, column=1, padx=10, pady=5)

    total_length_label = Label(root, text="Lungimea totala a parolei:")
    total_length_label.grid(row=7, column=0, padx=10, pady=5)
    total_length_entry = Entry(root, width=10)
    total_length_entry.grid(row=7, column=1, padx=10, pady=5)

    # Lista de parole
    password_label = Label(root, text="Parole generate:")
    password_label.grid(row=8, column=0, padx=10, pady=5)
    password_listbox = Listbox(root, width=50, height=10)
    password_listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    # Genereaza parole button
    generate_button = Button(root, text="Genereaza Parole", command=generate_passwords)
    generate_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

def generate_password(min_alpha, max_alpha, min_numeric, max_numeric, min_special, max_special, total_length):
    # Crearea parametrilor LFSR
    lfsr_length = 16
    lfsr_taps = [13, 14, 15, 16]

    # Generarea secventei LFSR
    lfsr_sequence = [1] * lfsr_length
    for i in range(lfsr_length, total_length):
        new_bit = lfsr_sequence[lfsr_taps[0] - 1] ^ lfsr_sequence[lfsr_taps[1] - 1] ^ lfsr_sequence[lfsr_taps[2] - 1] ^ lfsr_sequence[lfsr_taps[3] - 1]
        lfsr_sequence.append(new_bit)
        lfsr_sequence.pop(0)  # Eliminăm cel mai vechi bit din secvență

    # Calcularea numarului de caractere necesare pentru fiecare categorie
    alpha_count = sum(lfsr_sequence[:total_length].count(bit) for bit in [0, 1]) % (max_alpha - min_alpha + 1) + min_alpha
    numeric_count = sum(lfsr_sequence[:total_length].count(bit) for bit in [1]) % (max_numeric - min_numeric + 1) + min_numeric
    special_count = sum(lfsr_sequence[:total_length].count(bit) for bit in [0]) % (max_special - min_special + 1) + min_special

    # Calculează numărul de caractere rămase și ajustează numărul de caractere alfanumerice.
    remaining_count = total_length - alpha_count - numeric_count - special_count
    alpha_count += remaining_count if remaining_count >= 0 else 0

    # Generarea caracterelor pentru parolă
    alpha_chars = ''.join(random.choices(string.ascii_letters, k=alpha_count))
    numeric_chars = ''.join(random.choices(string.digits, k=numeric_count))
    special_chars = ''.join(random.choices(string.punctuation, k=special_count))

    # Combina și amestecă caracterele
    password = ''.join(random.sample(alpha_chars + numeric_chars + special_chars, total_length))

    return password

#Definim functia generate_passwords (ATENTIE generate_passwords si generate_password sunt functii diferite)


def generate_passwords():
    global min_alpha_entry, max_alpha_entry, min_numeric_entry, max_numeric_entry, \
           min_special_entry, max_special_entry, total_length_entry

    # Stergem parolele anterioare
    password_listbox.delete(0, END)

    # Luam valorile de la fiecare formular(input)
    min_alpha = int(min_alpha_entry.get())
    max_alpha = int(max_alpha_entry.get())
    min_numeric = int(min_numeric_entry.get())
    max_numeric = int(max_numeric_entry.get())
    min_special = int(min_special_entry.get())
    max_special = int(max_special_entry.get())
    total_length = int(total_length_entry.get())

    # Generam parolele si le afisam in listbox
    for i in range(50):
        password = generate_password(min_alpha, max_alpha, min_numeric, max_numeric, min_special, max_special, total_length)
        password_listbox.insert(END, password)


if __name__ == '__main__':
    create_gui()