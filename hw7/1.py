import psycopg2
from tkinter import *

class Autori:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="autori",  
                user="postgres",   
                password="postgres", 
                host="localhost",    
                port="5432"      
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Ошибка подключения к базе данных:", e)
            return
        
        self.window = Tk()
        self.window.geometry('400x400+300+100') 
        self.window.title('autoriii')  
        
        self.window.configure(bg='black')
        window_width = 400
        window_height = 400
        center_x = window_width // 2
        center_y = window_height // 2
     
        self.L1 = Label(self.window, text='Login', fg='white', bg='black', font=('Times New Roman', 14))
        self.L2 = Label(self.window, text='Password', fg='white', bg='black', font=('Times New Roman', 14))
        self.L1.place(x=center_x - 40, y=center_y - 60)
        self.L2.place(x=center_x - 50, y=center_y)
        self.E1 = Entry(self.window, font=('Times New Roman', 14))
        self.E2 = Entry(self.window, show='*', font=('Times New Roman', 14)) 
        self.E1.place(x=center_x - 50, y=center_y - 30)
        self.E2.place(x=center_x - 50, y=center_y + 30)
        self.B = Button(self.window, text='Enter', fg='black', bg='white', font=('Times New Roman', 12))
        self.B.place(x=center_x - 40, y=center_y + 80)
        
        self.B.bind('<Button-1>', self.check_log_pass)

    def success_enter(self):
        self.window.destroy()
        new_window = Tk()
        new_window.geometry('400x400+300+100') 
        new_window.configure(bg='black')
        L3 = Label(new_window, text='Success! Welcome!', fg='white', bg='black', font=('Times New Roman', 16))
        L3.pack(side=LEFT)

    def not_success_enter(self):
        error_window = Tk()
        error_window.geometry('400x400+300+100') 
        error_window.configure(bg='black')
        L4 = Label(error_window, text='Wrong login or password', fg='white', bg='black', font=('Times New Roman', 16))
        L4.pack(side=LEFT)

    def check_log_pass(self, event):
        login = self.E1.get()
        password = self.E2.get()
        query = "SELECT * FROM passwords WHERE username = %s AND password = %s"
        self.cursor.execute(query, (login, password))
        result = self.cursor.fetchone()

        if result:
            self.success_enter()  
        else:
            self.not_success_enter() 

    def mainloop(self):
        self.window.mainloop()

result = Autori()
result.mainloop()
