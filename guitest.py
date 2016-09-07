import datetime
from tkinter import *
from tkinter import messagebox

import mysql.connector

__author__ = 'hiperbolt'
cnx = mysql.connector.connect(user='root', password='01122rfg@', host='127.0.0.1', database='logininfo')
cursor = cnx.cursor()


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


class login():
    def __init__(self):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Username:')
        self.label2 = Label(self.frame2, text='Password:')
        self.button1 = Button(self.frame2, text='Login', command=lambda: self.loginconfirm())
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.button1.pack()

    def loginconfirm(self):
        global inputusername
        inputusername = self.entry1.get()
        inputpassword = self.entry2.get()
        query = ("SELECT * FROM credentials "
                 "WHERE username= %s AND password= %s")

        cursor.execute(query, (inputusername, inputpassword))

        if len(cursor.fetchall()) == 0:
            messagebox.showerror("Sign-In Error", "Wrong username/password combination!")
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.label1.pack_forget()
            self.label2.pack_forget()
            self.entry1.pack_forget()
            self.entry2.pack_forget()
            self.button1.pack_forget()
            login()
        else:
            login.loginsection(self)

    def loginsection(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.label1.pack_forget()
        self.label2.pack_forget()
        self.entry1.pack_forget()
        self.entry2.pack_forget()
        self.button1.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.label1 = Label(self.frame1, text='Hello ' + inputusername + '!')
        self.button1 = Button(self.frame2, text='Change password', command=lambda: login.changepassword(self))
        self.button2 = Button(self.frame2, text='Logout', command=lambda: login.logout(self))
        self.button3 = Button(self.frame2, text='Delete', command=lambda: login.delete(self))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()

    def changepassword(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.label1.pack_forget()
        self.label2.pack_forget()
        self.entry1.pack_forget()
        self.entry2.pack_forget()
        self.button1.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.entry3 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Old Password:')
        self.label2 = Label(self.frame2, text='New Password:')
        self.label3 = Label(self.frame2, text='Re-Enter New Password:')
        self.button1 = Button(self.frame2, text='Change password', command=lambda: self.changepasswordconfirm())
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.button1.pack()

    def changepasswordconfirm(self):
        query = ("SELECT * FROM credentials WHERE username= %s AND password= %s;")

        self.oldpassword = self.entry1.get()
        self.newpassword = self.entry2.get()
        self.newpassword2 = self.entry3.get()

        cursor.execute(query, (inputusername, self.oldpassword))
        if len(cursor.fetchall()) == 0:
            messagebox.showerror("Wrong password!", "The password entered is incorrect!")
            login.changepassword(self)
        else:
            if self.newpassword == self.newpassword2:
                update_password = ("UPDATE credentials SET password = %s WHERE username = %s")
                cursor.execute(update_password, (self.newpassword, inputusername))
                cnx.commit()
                messagebox.showinfo("Sucess!", "Password was altered sucessfully!")
                login.loginsection(self)
            else:
                messagebox.showerror("Password don't match!", "The password do not match!")
                login.changepassword(self)

    def logout(self):
        cursor.close()
        cnx.close()
        root.quit()

    def delete(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.label1.pack_forget()
        self.label2.pack_forget()
        self.entry1.pack_forget()
        self.entry2.pack_forget()
        self.button1.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.label1 = Label(self.frame1, text='Enter your password:')
        self.entry1 = Entry(self.frame2)
        self.button1 = Button(self.frame2, text='Delete!', command=lambda: login.deleteconfirm(self))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.entry1.pack()
        self.button1.pack()

    def deleteconfirm(self):
        query = ("SELECT * FROM credentials WHERE username= %s AND password= %s;")

        password = self.entry1.get()
        cursor.execute(query, (inputusername, password))
        if len(cursor.fetchall()) == 0:
            messagebox.showerror("Error!", "Wrong password!")
            login.delete(self)
        else:
            delete_account = ("DELETE FROM credentials WHERE username= %s")
            cursor.execute(delete_account, (inputusername,))
            messagebox.showinfo("Sucess!", 'Your account has been deleted!')
            cnx.commit()
            cursor.close()
            cnx.close()
            root.quit()


class register():
    def __init__(self):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.entry3 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Username:')
        self.label2 = Label(self.frame2, text='Password:')
        self.label3 = Label(self.frame2, text='Re-Enter Password:')
        self.button1 = Button(self.frame2, text='Register', command=lambda: self.registerconfirm())
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.button1.pack()

    def registerconfirm(self):
        query = ("SELECT * FROM credentials "
                 "WHERE username= %s")
        desiredusername = self.entry1.get()
        desiredpassword = self.entry2.get()
        desiredpassword2 = self.entry3.get()
        cursor.execute(query, (desiredusername,))
        if len(cursor.fetchall()) == 0:
            if desiredpassword2 == desiredpassword:
                add_credential = ("INSERT INTO credentials "
                                  "(username, password, created) "
                                  "VALUES (%s, %s, %s)")
                cursor.execute(add_credential, (desiredusername, desiredpassword, str(datetime.date.today())))
                cnx.commit()
                root.quit()
                cursor.close()
                cnx.close()
            else:
                messagebox.showerror("Password don't match!", "The password do not match!")
        else:
            messagebox.showerror("Username Unavailable!", "This username is taken!")
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.label1.pack_forget()
            self.label2.pack_forget()
            self.entry1.pack_forget()
            self.entry2.pack_forget()
            self.label3.pack_forget()
            self.entry3.pack_forget()
            self.button1.pack_forget()
            register()


def initialscreen():
    root.geometry('500x400')
    root.title('ArchMaint')
    frame1 = Frame(root)
    frame2 = Frame(root)
    label1 = Label(frame1, text='Welcome to the login program!', font=5)
    button1 = Button(frame2, text='Login',
                     command=lambda: combine_funcs(button2.pack_forget(), button1.pack_forget(), login()))
    button2 = Button(frame2, text='Register',
                     command=lambda: combine_funcs(button2.pack_forget(), button1.pack_forget(), register()))
    frame1.pack()
    frame2.pack()
    label1.pack()
    button1.pack()
    button2.pack()
    root.mainloop()


root = Tk()
initialscreen()
