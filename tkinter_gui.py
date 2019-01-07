from tkinter import *
from threading import Thread
from Client.Client import Client


class ClientGUI(Client):

    def __init__(self):

        self.window = Tk()
        self.window.title("ChatClient")
        self.window.geometry("800x600")
        send_message_line_height = 25
        text_windows_width = 560
        second_column_start = 580
        second_column_width = 200

        self.message_input = Text(self.window).place(x=10, y=570, width=text_windows_width,
                                                     height=send_message_line_height)

        self.send_message_button = Button(self.window, text="Send message")
        self.send_message_button.place(x=second_column_start, y=570,
                                       width=second_column_width, height=send_message_line_height)

        self.messages_output = Text(self.window).place(x=10, y=10,
                                                       width=text_windows_width, height=550)

        self.login_input = Text(self.window).place(x=second_column_start, y=10,
                                                   width=second_column_width, height=send_message_line_height)

        self.accept_login_button = Button(self.window, text="Accept Login")
        self.accept_login_button.place(x=second_column_start, y=50,
                                       width=second_column_width, height=send_message_line_height)

        self.window.mainloop()


a = ClientGUI()
