from tkinter import *
from threading import Thread
from Client.Client import Client
from tkinter import messagebox


class ClientGUI(Client):

    connection_is_active = False

    def __init__(self):

        self.print_messages_thread = Thread(target=self.print_received_messages)
        self.window = Tk()
        self.window.title("ChatClient")
        self.window.geometry("800x600")
        send_message_line_height = 25
        text_windows_width = 560
        second_column_start = 580
        second_column_width = 200

        self.message_input = Text(self.window)
        self.message_input.place(x=10, y=570, width=text_windows_width,
                                                     height=send_message_line_height)

        self.send_message_button = Button(self.window, text="Send message", command=self.send_message_button_clicked)
        self.send_message_button.place(x=second_column_start, y=570,
                                       width=second_column_width, height=send_message_line_height)

        self.messages_output = Text(self.window)
        self.messages_output.place(x=10, y=10,
                                   width=text_windows_width, height=550)

        self.login_input = Text(self.window)
        self.login_input.place(x=second_column_start, y=10,
                                                   width=second_column_width, height=send_message_line_height)

        self.accept_login_button = Button(self.window, text="Accept Login",  relief=GROOVE, command=self.accept_login_button_clicked)
        self.accept_login_button.place(x=second_column_start, y=50,
                                       width=second_column_width, height=send_message_line_height)

        self.window.mainloop()

    def accept_login_button_clicked(self):

        user_login = self.login_input.get("1.0", END)

        if not self.__is_login_input_empty__():
            Client.__init__(self, user_login)
            self.print_messages_thread.start()
            print(user_login)
        else:
            messagebox.showerror("No login", "Input Login!")

    def __is_login_input_empty__(self) -> bool:
        return self.login_input.compare("end-1c", "==", "1.0")

    def send_message_button_clicked(self):
        self.send_message(self.message_input.get("1.0", END))
        self.print_received_messages()

    def print_received_messages(self):
        self.messages_output.insert(END, str(self.messages_history))


a = ClientGUI()
