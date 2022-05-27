import socket
import threading
import tkinter as tk
from tkinter import END
from client import Client
from server import Server

specials = {
    " ": "|<SPACE>|",
    "¬": "|<NEGATION>|",
    "¦": "|<SPLITPIPE>|",
    "`": "|<BACKQUOTE>|",
    '"': "|<QUOTE>|",
    "£": "|<QUID>|",
    "$": "|<DOLLAR>|",
    "€": "|<EURO>|",
    "%": "|<PERCENT>|",
    "^": "|<CARAT>|",
    "&": "|<AMPERSAND>|",
    "+": "|<PLUS>|",
    "=": "|<EQUALS>|",
    "[": "|<OPENSQUARE>|",
    "]": "|<CLOSESQUARE>|",
    "{": "|<OPENCURLY>|",
    "}": "|<CLOSECURLY>|",
    ":": "|<COLON>|",
    ";": "|<SEMI>|",
    "@": "|<AT>|",
    "#": "|<HASH>|",
    "/": "|<SLASH>|",
    "?": "|<QUESTION>|",
    ",": "|<COMMA>|",
    "\\": "|<BACKSLASH|>"
}

SEPARATOR = "|<SEPARATOR>|"
STOPMESSAGE = "#64STOPorAng3"

class TkinterWindow(tk.Tk):
    def __init__(self, window_x:int=640, window_y:int=512, offset_x=0, offset_y=0):
        super().__init__()
        self.title("Chat")
        self.geometry(f"{window_x}x{window_y}+{offset_x}+{offset_y}")

        self.messagebox = tk.Text(self, width=68, font=0)
        self.textbox = tk.Entry(self, width=68, font=0)

        self.messagebox.pack(expand=True)
        self.textbox.pack(expand=True)

        self.messagebox['state'] = "disabled"
        self.textbox.focus()

    def update(self, name, text):
        self.messagebox['state'] = "normal"
        self.messagebox.insert(END, chars=f"{name}:\n{text}\n\n")
        self.messagebox['state'] = "disabled"
        self.messagebox.yview_moveto(1)
        self.textbox.delete(0,END)


class Chat:
    def __init__(self, ip: str, port: int=8000):
        self.isrunning = True
        self.host = False
        self.window = TkinterWindow()
        self.server = Server(port)
        self.client = Client(ip, port)

        self.serverthread = threading.Thread(target=self.serverstart, daemon=True)
        self.receiver = threading.Thread(target=self.receive, daemon=True)

        if ip == socket.gethostbyname(socket.gethostname()) or ip == "localhost" or ip[0:3] == "127" or ip == "0.0.0.0":
            self.serverthread.start()
            self.host = True
        self.receiver.start()

        self.window.textbox.bind("<Return>", self.sendevent)

    def receive(self):
        info = []
        previnfo = []
        if self.host:
            while self.isrunning:
                try:
                    info = self.server.download().split(SEPARATOR)[:-1]
                    if info != previnfo:
                        newdata = info[len(previnfo):]
                        previnfo = info
                        for newthing in newdata:
                            name, message = newthing.split("/")
                            for special in specials: message = message.replace(specials[special], special)
                            self.window.update(name, message)
                except: pass
        else:
            while self.isrunning:
                try:
                    info = self.client.request().split(SEPARATOR)[:-1]
                    if info != previnfo:
                        newdata = info[len(previnfo):]
                        previnfo = info
                        for newthing in newdata:
                            name, message = newthing.split("/")
                            for special in specials: message = message.replace(specials[special], special)
                            self.window.update(name, message)
                except: pass

    def send(self):
        msg = self.window.textbox.get()
        if msg == "EXIT":
            self.isrunning = False
            self.window.destroy()
            if self.host: 
                self.server.upload(NAME, STOPMESSAGE)
                # self.server.stop()
                self.serverthread.join()
            else: self.client.send(NAME, STOPMESSAGE)
        else:
            for special in specials: msg = msg.replace(special, specials[special])
            if self.host: self.server.upload(NAME, msg)
            else: self.client.send(NAME, msg)

    def sendevent(self, event=None): self.send()
    def serverstart(self): self.server.start()


NAME = input("Input your name: ")


chat = Chat("127.0.0.1", 8000)
chat.window.mainloop()
