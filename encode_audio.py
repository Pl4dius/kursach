import wave
import struct
import numpy as np
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def encode_message(audio_path, message, output_path):
    with wave.open(audio_path, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    binary_message = text_to_bits(message) + '1111111111111110'
    if len(binary_message) > len(frames):
        raise ValueError("Сообщение слишком длинное для данного аудиофайла.")

    for i in range(len(binary_message)):
        frames[i] = (frames[i] & 254) | int(binary_message[i])

    with wave.open(output_path, 'wb') as encoded_audio:
        encoded_audio.setparams(audio.getparams())
        encoded_audio.writeframes(frames)

    messagebox.showinfo("Успех", f"Сообщение закодировано и сохранено в {output_path}")

def select_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Wave files", "*.wav")])
    if file_path:
        audio_path_entry.delete(0, "end")
        audio_path_entry.insert(0, file_path)

def save_audio():
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave files", "*.wav")])
    if file_path:
        output_path_entry.delete(0, "end")
        output_path_entry.insert(0, file_path)

def encode():
    try:
        encode_message(audio_path_entry.get(), message_entry.get(), output_path_entry.get())
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создаем GUI
root = Tk()
root.title("Скрытие сообщения в аудиофайле")

Label(root, text="Путь к аудиофайлу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
audio_path_entry = Entry(root, width=50)
audio_path_entry.grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Выбрать...", command=select_audio).grid(row=0, column=2, padx=5, pady=5)

Label(root, text="Сообщение:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
message_entry = Entry(root, width=50)
message_entry.grid(row=1, column=1, padx=5, pady=5)

Label(root, text="Сохранить как:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
output_path_entry = Entry(root, width=50)
output_path_entry.grid(row=2, column=1, padx=5, pady=5)
Button(root, text="Сохранить...", command=save_audio).grid(row=2, column=2, padx=5, pady=5)

Button(root, text="Закодировать", command=encode).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()