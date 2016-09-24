from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from tkinter import ttk


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func

def forthwindow():
    label1 = Label(text="Finished!", font=("Areal", 16), background='white')
    label2 = Message(
        text="Installation Wizard has finished installing loginsystem.",
        width=467, background='white')
    button3 = Button(text="Finish", command=lambda: sys.exit(0))
    label1.place(x=173, y=10)
    label2.place(x=172, y=38)
    button3.place(x=560, y=310)

def thirdwindow(username, password):
    label1 = Label(text="Configuring MySQL Database...", font=("Areal", 16), background='white')
    label2 = Message(
        text="This shouldn't take much time.",
        width=467, background='white')
    progressbar1 = ttk.Progressbar(orient="horizontal", length=200, mode="indeterminate")

    label1.place(x=173, y=10)
    label2.place(x=172, y=38)
    progressbar1.place(x=172, y=160)
    progressbar1.start(50)

    cnx = mysql.connector.connect(user='root', password='01122rfg@', host='127.0.0.1')
    cursor = cnx.cursor()

    DB_NAME = 'logininfo'

    database = "CREATE DATABASE logininfo;"
    cursor.execute(database)

    cursor.close()
    cnx.close()

    cnx = mysql.connector.connect(user=username, password=password, host='127.0.0.1', database=DB_NAME)
    cursor = cnx.cursor()
    query = (
        "CREATE TABLE 'credentials' ("
        "  'username' varchar(20) NOT NULL"
        "  'email' varchar(60) NOT NULL"
        "  'created' date NOT NULL"
        "  'twostepauth' varchar(20) NOT NULL"
        "  'phonenumber' varchar(60) NOT NULL"
        "  'iterations' varchar(20) NOT NULL"
        "  'salt' varchar(80) NOT NULL"
        "  'hash' varchar(300) NOT NULL"
        ") ENGINE=InnoDB")

    table = (
        "CREATE TABLE credentials (username varchar(20) NULL, email varchar(60) NULL, created date NULL, twostepauth varchar(20) NULL, phonenumber varchar(60) NULL, iterations varchar(20) NULL, salt varchar(80) NULL, hash varchar(300) NULL)")

    table2 = ("CREATE TABLE passwordrecover (Date date, username varchar(20))")

    cursor.execute(table)
    cursor.execute(table2)
    cursor.close()
    cnx.close()
    label1.place_forget()
    label2.place_forget()
    progressbar1.place_forget()
    forthwindow()

def secondwindow():
    label1 = Label(text="Configure MySQL", font=("Areal", 16), background='white')
    label2 = Message(
        text="Configure Login System's access to your MySQL Database. Click Skip if you don't have MySQL configured yet.",
        width=467, background='white')
    button1 = Button(text="Skip", command=lambda: thirdwindow())
    button2 = Button(text="Next", command=lambda: secondwindow_get())
    button3 = Button(text="Cancel", command=lambda: sys.exit(0))
    label3 = Label(text="MySQL username (Usually 'root'):", background='white')
    label4 = Label(text="MySQL password (For the user you choose):", background='white')
    entry1 = Entry()
    entry2 = Entry()

    label1.place(x=173, y=10)
    label2.place(x=172, y=38)
    label3.place(x=172, y=100)
    label4.place(x=172, y=160)
    entry1.place(x=172, y=120)
    entry2.place(x=172, y=180)
    button1.place(x=420, y=310)
    button2.place(x=490, y=310)
    button3.place(x=560, y=310)

    def secondwindow_get():
        mysql_username = entry1.get()
        mysql_password = entry2.get()
        label1.place_forget()
        label2.place_forget()
        label3.place_forget()
        label4.place_forget()
        entry1.place_forget()
        entry2.place_forget()
        button1.place_forget()
        button2.place_forget()
        button3.place_forget()
        thirdwindow(mysql_username, mysql_password)


def firstwindow():
    root.geometry('640x350')
    root.title('Install Login system 0.0.10 (64-bit)')
    background_image = ImageTk.PhotoImage(Image.open('/home/hiperbolt/Selecção_050.png'))
    image1 = Label(image=background_image)
    label1 = Label(text="Install Login system 0.0.10 (64-bit)", font=("Areal", 16), background='white')
    label2 = Message(
        text="Select Next to install Login System with default settings, or choose Customize to enable or disable"
             " features.",
        width=467, background='white')
    button1 = Button(text="Next",
                     command=lambda: combine_funcs(label1.place_forget(), label2.place_forget(), button1.place_forget(),
                                                   button2.place_forget(), secondwindow()))
    button2 = Button(text="Cancel", command=lambda: sys.exit(0))
    button1.config(highlightbackground='gray')
    button2.config(highlightbackground='gray')

    image1.place(x=0, y=0)
    label1.place(x=173, y=10)
    label2.place(x=172, y=38)
    button1.place(x=490, y=310)
    button2.place(x=560, y=310)

    root.mainloop()


root = Tk()
root.configure(background='white')
firstwindow()
