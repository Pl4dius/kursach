import wave
import struct
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def decode_message(audio_path):
    with wave.open(audio_path, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    binary_message = ""
    for i in range(len(frames)):
        binary_message += str(frames[i] & 1)

    decoded_message = bits_to_text(binary_message)
    stop_index = decoded_message.find(chr(255))
    if stop_index != -1:
        decoded_message = decoded_message[:stop_index]

    return decoded_message

def select_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Wave files", "*.wav")])
    if file_path:
        audio_path_entry.delete(0, "end")
        audio_path_entry.insert(0, file_path)

def decode():
    try:
        message = decode_message(audio_path_entry.get())
        messagebox.showinfo("Сообщение", f"Раскодированное сообщение: {message}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создаем GUI
root = Tk()
root.title("Извлечение сообщения из аудиофайла")

Label(root, text="Путь к аудиофайлу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
audio_path_entry = Entry(root, width=50)
audio_path_entry.grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Выбрать...", command=select_audio).grid(row=0, column=2, padx=5, pady=5)

Button(root, text="Декодировать", command=decode).grid(row=1, column=0, columnspan=3, pady=10)

root.mainloop()