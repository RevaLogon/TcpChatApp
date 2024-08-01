import socket
import threading
#import tkinter
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import json
#from tkinter import *
#from PIL import Image, ImageTk


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

HOST = IPAddr
PORT = 5000

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    #message_box.config(state=tk.DISABLED)

def connect():

    try:
        client.connect((HOST, PORT))
        print("Pigeon sizi basariyla server'a bagladi.")
        add_message("[SERVER] Bilgileriniz kontrol ediliyor...")
        add_message("[SERVER] Bilgileriniz doğru olunca server'a bağlanacaksınız.")
    except:
         print("yeni giriş")

    password = password_textbox.get()

    username = username_textbox.get()

    pack = {"usernameclient": username, "passwordclient": password}

    jsonPack = json.loads(json.dumps(pack).encode().decode())

    print(jsonPack)

    if username != '' and password != '':
        client.sendall(json.dumps(pack).encode())
        username_textbox.delete(0, len(username))
        password_textbox.delete(0, len(password))
        message_textbox.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Hata!",f"Kullanıcı adınızı ve şifrenizi boş bırakmayınız.")



    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()



def send_message():
    message = message_textbox.get()
    if message != '':

        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Boş mesaj", "Ileti boş birakilamaz.")


root = tk.Tk()
root.geometry("600x600")
root.title("Pigeon MSG")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

#C = Canvas(root, bg="blue", height=100, width=100)
#filename = PhotoImage(file = "pigeon_PNG54606.png")
#background_label = Label(root, image=filename)
#background_label.place(x=0, y=0, relwidth=2, relheight=1)


top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

top2_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top2_frame.grid(row=1, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=2, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=3, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Isim Giriniz:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
username_textbox.pack(side=tk.LEFT)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=36)
message_textbox.pack(side=tk.LEFT, padx=10)
message_textbox.config(state=tk.DISABLED)

message_button = tk.Button(bottom_frame, text="Gönder", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
#message_button.bind('<Return>', send_message)
message_button.pack(side=tk.LEFT, padx=10)
message_button.config(state=tk.DISABLED)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

password_label = tk.Label(top2_frame, text="Şifre Giriniz:", font=FONT, bg=DARK_GREY, fg=WHITE)
password_label.pack(side=tk.LEFT, padx=10)

password_textbox = tk.Entry(top2_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
password_textbox.pack(side=tk.LEFT)

password_button = tk.Button(top2_frame, text="Gir", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
password_button.pack(side=tk.LEFT, padx=15)




def listen_for_messages_from_server(client):

    while 1:

        message = (client.recv(4096).decode('UTF-8'))
        print(message)
        if message != '':
            message_button.config(state=tk.NORMAL)
            message_textbox.config(state=tk.NORMAL)
            a = username_textbox.get()
            print(f"message received: {message}")
            username = message.split("~")[0]
            content = message.split('~')[1]
            print(username)
            add_message(f"[{username}] {content}")
            username_textbox.config(state=tk.DISABLED)
            password_textbox.config(state=tk.DISABLED)
            password_button.config(state=tk.DISABLED)

            continue
        else:
            messagebox.showerror("Hata", "Kullanici'nin ilettigi gonderi bos.")

def main():

    root.mainloop()

if __name__ ==  '__main__':
    main()
