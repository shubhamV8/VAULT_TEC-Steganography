from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import os

class Stegno:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Steganography')
        self.root.geometry('500x600')
        self.create_main_frame()

    def create_main_frame(self):
        frame = Frame(self.root)
        frame.pack()

        Label(frame, text='Image Steganography', font=('courier', 33)).grid(pady=10)
        Button(frame, text="Encode", command=self.encode_frame, font=('courier', 14)).grid(pady=12)
        Button(frame, text="Decode", command=self.decode_frame, font=('courier', 14)).grid(pady=12)
        Label(frame, text='¯\\_(ツ)_/¯', font=('courier', 60)).grid(pady=10)

    def encode_frame(self):
        self.clear_frame()
        frame = Frame(self.root)
        frame.pack()

        Label(frame, text='Select Image to Hide Text:', font=('courier', 18)).grid()
        Button(frame, text='Select', command=lambda: self.select_image(frame, encode=True), font=('courier', 14)).grid()
        Button(frame, text='Cancel', command=self.create_main_frame, font=('courier', 14)).grid(pady=15)

    def decode_frame(self):
        self.clear_frame()
        frame = Frame(self.root)
        frame.pack()

        Label(frame, text='Select Image with Hidden Text:', font=('courier', 18)).grid()
        Button(frame, text='Select', command=lambda: self.select_image(frame, encode=False), font=('courier', 14)).grid()
        Button(frame, text='Cancel', command=self.create_main_frame, font=('courier', 14)).grid(pady=15)

    def select_image(self, frame, encode):
        file_path = filedialog.askopenfilename(filetypes=[('Images', '*.png;*.jpg;*.jpeg')])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((300, 200))
            img_tk = ImageTk.PhotoImage(img)
            Label(frame, image=img_tk).grid()
            if encode:
                self.encode_text(frame, img)
            else:
                self.decode_text(img)

    def encode_text(self, frame, img):
        Label(frame, text='Enter message:', font=('courier', 18)).grid(pady=15)
        text_area = Text(frame, width=50, height=10)
        text_area.grid()
        Button(frame, text='Encode', command=lambda: self.encode(img, text_area.get("1.0", "end-1c")), font=('courier', 11)).grid(pady=15)

    def decode_text(self, img):
        hidden_data = self.decode(img)
        messagebox.showinfo("Decoded Message", hidden_data)

    def encode(self, img, data):
        if not data.strip():
            messagebox.showwarning("Input Error", "Please enter text to encode.")
            return

        encoded_img = img.copy()
        data_bin = ''.join(format(ord(i), '08b') for i in data) + '11111111'  # End delimiter
        pixels = list(encoded_img.getdata())
        
        for i in range(len(data_bin)):
            r, g, b = pixels[i]
            if data_bin[i] == '1':
                r |= 1
            else:
                r &= ~1
            pixels[i] = (r, g, b)

        encoded_img.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG files', '*.png')])
        if save_path:
            encoded_img.save(save_path)
            messagebox.showinfo("Success", "Text encoded successfully!")

    def decode(self, img):
        data = ''
        pixels = list(img.getdata())
        for pixel in pixels:
            data += str(pixel[0] & 1)
            if data[-8:] == '11111111':  # Check for end delimiter
                break
        return ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data)-8, 8))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Stegno(root)
    root.mainloop()

