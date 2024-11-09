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
        self.window.geometry('500x500+300+100') 
        self.window.title('autoriii')  
        
        self.window.configure(bg='black')

        #фон
        self.bg_image = PhotoImage(file=r"C:\Users\ASUS\Desktop\python2\hw7\bg.png")  # Укажите путь к изображению фона
        bg_label = Label(self.window, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

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

        #кнопки для доп действий
        self.new_user_button = Button(self.window, text="New User", fg='black', bg='white', font=('Times New Roman', 12), command=self.create_new_user)
        self.new_user_button.place(x=center_x - 40, y=center_y + 120)

        self.change_password_button = Button(self.window, text="Change Password", fg='black', bg='white', font=('Times New Roman', 12), command=self.change_password)
        self.change_password_button.place(x=center_x - 50, y=center_y + 160)

        self.change_login_button = Button(self.window, text="Change Login", fg='black', bg='white', font=('Times New Roman', 12), command=self.change_login)
        self.change_login_button.place(x=center_x - 50, y=center_y + 200)

        self.delete_user_button = Button(self.window, text="Delete User", fg='black', bg='white', font=('Times New Roman', 12), command=self.delete_user)
        self.delete_user_button.place(x=center_x - 50, y=center_y + 240)

    def success_enter(self):
        self.window.destroy()
        new_window = Tk()
        new_window.geometry('400x400+300+100') 
        new_window.configure(bg='black')

        #изображение
        success_image = PhotoImage(file=r"C:\Users\ASUS\Desktop\python2\hw7\success.png")
        success_label = Label(new_window, image=success_image, bg='black')
        success_label.image = success_image 
        success_label.pack(pady=30)

        L3 = Label(new_window, text='Success! Welcome!', fg='white', bg='black', font=('Times New Roman', 16))
        L3.pack(side=LEFT)

    def not_success_enter(self):
        error_window = Tk()
        error_window.geometry('500x500+300+100') 
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

    def create_new_user(self):
        def submit_new_user():
            login = new_login_entry.get()
            password = new_password_entry.get()

            #проверка на сущ лог
            self.cursor.execute("SELECT * FROM passwords WHERE username = %s", (login,))
            if self.cursor.fetchone():
                error_label.config(text="Login already exists!")
            else:
                self.cursor.execute("INSERT INTO passwords (username, password) VALUES (%s, %s)", (login, password))
                self.conn.commit()
                success_label.config(text="User created successfully!")

        new_user_window = Toplevel(self.window)
        new_user_window.geometry('500x500+300+100')
        new_user_window.configure(bg='black')
        Label(new_user_window, text="New Username", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        new_login_entry = Entry(new_user_window, font=('Times New Roman', 14))
        new_login_entry.pack(pady=10)

        Label(new_user_window, text="New Password", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        new_password_entry = Entry(new_user_window, show='*', font=('Times New Roman', 14))
        new_password_entry.pack(pady=10)

        submit_button = Button(new_user_window, text="Submit", fg='black', bg='white', font=('Times New Roman', 12), command=submit_new_user)
        submit_button.pack(pady=20)

        error_label = Label(new_user_window, fg='red', bg='black', font=('Times New Roman', 12))
        error_label.pack()

        success_label = Label(new_user_window, fg='green', bg='black', font=('Times New Roman', 12))
        success_label.pack()

    def change_password(self):
        def submit_change_password():
            login = change_login_entry.get()
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()

            #проверка
            self.cursor.execute("SELECT * FROM passwords WHERE username = %s AND password = %s", (login, old_password))
            if self.cursor.fetchone():
                self.cursor.execute("UPDATE passwords SET password = %s WHERE username = %s", (new_password, login))
                self.conn.commit()
                success_label.config(text="Password changed successfully!")
            else:
                error_label.config(text="Incorrect login or password!")

        change_password_window = Toplevel(self.window)
        change_password_window.geometry('500x500+300+100')
        change_password_window.configure(bg='black')

        Label(change_password_window, text="Login", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        change_login_entry = Entry(change_password_window, font=('Times New Roman', 14))
        change_login_entry.pack(pady=10)

        Label(change_password_window, text="Old Password", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        old_password_entry = Entry(change_password_window, show='*', font=('Times New Roman', 14))
        old_password_entry.pack(pady=10)

        Label(change_password_window, text="New Password", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        new_password_entry = Entry(change_password_window, show='*', font=('Times New Roman', 14))
        new_password_entry.pack(pady=10)

        submit_button = Button(change_password_window, text="Submit", fg='black', bg='white', font=('Times New Roman', 12), command=submit_change_password)
        submit_button.pack(pady=20)

        error_label = Label(change_password_window, fg='red', bg='black', font=('Times New Roman', 12))
        error_label.pack()

        success_label = Label(change_password_window, fg='green', bg='black', font=('Times New Roman', 12))
        success_label.pack()

    def change_login(self):
        def submit_change_login():
            old_login = old_login_entry.get()
            new_login = new_login_entry.get()

            #проверка
            self.cursor.execute("SELECT * FROM passwords WHERE username = %s", (new_login,))
            if self.cursor.fetchone():
                error_label.config(text="Login already exists!")
            else:
                self.cursor.execute("UPDATE passwords SET username = %s WHERE username = %s", (new_login, old_login))
                self.conn.commit()
                success_label.config(text="Login changed successfully!")

        change_login_window = Toplevel(self.window)
        change_login_window.geometry('500x500+300+100')
        change_login_window.configure(bg='black')

        Label(change_login_window, text="Old Login", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        old_login_entry = Entry(change_login_window, font=('Times New Roman', 14))
        old_login_entry.pack(pady=10)

        Label(change_login_window, text="New Login", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        new_login_entry = Entry(change_login_window, font=('Times New Roman', 14))
        new_login_entry.pack(pady=10)

        submit_button = Button(change_login_window, text="Submit", fg='black', bg='white', font=('Times New Roman', 12), command=submit_change_login)
        submit_button.pack(pady=20)

        error_label = Label(change_login_window, fg='red', bg='black', font=('Times New Roman', 12))
        error_label.pack()

        success_label = Label(change_login_window, fg='green', bg='black', font=('Times New Roman', 12))
        success_label.pack()

    def delete_user(self):
        def submit_delete_user():
            login = delete_login_entry.get()
            self.cursor.execute("DELETE FROM passwords WHERE username = %s", (login,))
            self.conn.commit()
            success_label.config(text="User deleted successfully!")

        delete_user_window = Toplevel(self.window)
        delete_user_window.geometry('500x500+300+100')
        delete_user_window.configure(bg='black')

        Label(delete_user_window, text="Login", fg='white', bg='black', font=('Times New Roman', 14)).pack(pady=10)
        delete_login_entry = Entry(delete_user_window, font=('Times New Roman', 14))
        delete_login_entry.pack(pady=10)

        submit_button = Button(delete_user_window, text="Submit", fg='black', bg='white', font=('Times New Roman', 12), command=submit_delete_user)
        submit_button.pack(pady=20)

        success_label = Label(delete_user_window, fg='green', bg='black', font=('Times New Roman', 12))
        success_label.pack()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    user_app = Autori()
    user_app.window.mainloop()
