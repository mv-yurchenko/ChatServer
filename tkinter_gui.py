import tkinter as tk
from threading import Thread
from Client.Client import Client





def foo(thread_num):
    for i in range(100):
        print(i)
        tex.insert(tk.END, str(thread_num) + " : " + str(i) + "\n")
        tex.see(tk.END)


t1 = Thread(target=foo, args=[1])
t2 = Thread(target=foo, args=[2])
t1.start()
t2.start()


top.mainloop()