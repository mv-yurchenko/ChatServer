from tkinter import *
from threading import Thread

tk=Tk()

text=StringVar()
name=StringVar()
name.set('HabrUser')
text.set('')
tk.title('MegaChat')
tk.geometry('400x300')

log = Text(tk)
nick = Entry(tk, textvariable=name)
msg = Entry(tk, textvariable=text)
msg.pack(side='bottom', fill='x', expand='true')
nick.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both',expand='true')

tk.mainloop()
