import datetime
from tkinter import *
from tkinter import messagebox
import smtplib
import re

import mysql.connector

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import TwilioRestClient
import random
import bcrypt
from passlib.hash import pbkdf2_sha256
from sys import platform

if platform == "darwin":
    messagebox.showwarning("This program was not made to run in Mac OS / Darwin. We are not responsible for any eventual errors or malfunction.")
elif platform == "win32":
    messagebox.showerror("This program does NOT support Windows / win32 platforms. Exiting.")
    sys.exit(0)

### Variables - Change them to fit your needs:
use_two_step_authentication = 'false'  # Describes it self. True / False
accountSid = ""  # Twilio Account SID
auth_token = ""  # Twilio Authentication Token
client = TwilioRestClient(accountSid, auth_token)
__author__ = 'hiperbolt'  # Gotta get some o' that credit xd
cnx = mysql.connector.connect(user='', password='', host='127.0.0.1',
                              database='logininfo')  # MySQL Connector Information
cursor = cnx.cursor()
server = smtplib.SMTP('smtp.gmail.com', 587)  # Mail server, currently set to Gmail
server.starttls()
server.login('', '')  # Mail server credentials
link = "192.168.1.75/index.php" #Password Recovery Server Link
EMAIL_REGEX = re.compile(
    r"[^@]+@[^@]+\.[^@]+")  # In case you are curious, REGEX to make sure mail is valid, feel free to make a more comprehensive one


###

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


def to_integer(dt_time):
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day


class login():
    def __init__(self):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Username:')
        self.label2 = Label(self.frame2, text='Password:')
        self.button1 = Button(self.frame2, text='Login', command=lambda: self.loginconfirm())
        self.button2 = Button(self.frame2, text='Forgot password?', command=lambda: self.loginhelp())
        self.button3 = Button(self.frame2, text='Go back',
                              command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                            initialscreen()))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()

    def loginconfirm(self):
        global inputusername
        inputusername = self.entry1.get()
        inputpassword = self.entry2.get()
        query = ("SELECT * FROM credentials "
                 "WHERE username= %s")

        cursor.execute(query, (inputusername, ))

        if len(cursor.fetchall()) == 0:
            messagebox.showerror("Sign-In Error", "Wrong username!")
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            login()
        else:
            query = ("SELECT iterations, salt, hash FROM credentials WHERE username=%s")
            cursor.execute(query, (inputusername, ))
            for (iterations, salt, hash) in cursor:
                byted_salt = str.encode(salt)
                hash2 = pbkdf2_sha256.encrypt(inputpassword, rounds=int(iterations), salt=byted_salt)
                if hash2 == hash:
                    print('right password')
                else:
                    print('wrong password')
                    messagebox.showerror("Sign-In Error", "Wrong password!")
                    self.frame1.pack_forget()
                    self.frame2.pack_forget()
                    login()
                    return

            query = ("SELECT twostepauth FROM credentials WHERE username= %s")
            cursor.execute(query, (inputusername,))
            for (twostepauth) in cursor:
                if '0' in twostepauth:
                    login.loginsection(self)
                if '1' in twostepauth:
                    randomnumber = random.randint(0, 99999)

                    def checkrandomnumber():
                        inputrandomnumber = self.entry1.get()
                        if int(inputrandomnumber) == int(randomnumber):
                            login.loginsection(self)
                        else:
                            messagebox.showerror("Error", "Two-Step Authentication has failed!")
                            self.frame1.pack_forget()
                            self.frame2.pack_forget()
                            login()

                    query = "SELECT phonenumber FROM credentials WHERE username= %s"
                    cursor.execute(query, (inputusername,))
                    for (phonenumber) in cursor:
                        receiver = phonenumber

                    msg = "Here is your loginsystem acess code: %s" % str(randomnumber)
                    message = client.messages.create(to=receiver, from_="+16174090950", body=msg)
                    self.frame1.pack_forget()
                    self.frame2.pack_forget()
                    self.frame1 = Frame(root)
                    self.frame2 = Frame(root)
                    self.label1 = Label(self.frame1, text='Authentication Code:')
                    self.entry1 = Entry(self.frame2)
                    self.button1 = Button(self.frame2, text='Submit', command=lambda: checkrandomnumber())
                    self.frame1.pack()
                    self.frame2.pack()
                    self.label1.pack()
                    self.entry1.pack()
                    self.button1.pack()
                else:
                    login.loginsection(self)

    def loginhelp(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.label1 = Label(self.frame1, text='Enter username:')
        self.entry1 = Entry(self.frame1)
        self.button1 = Button(self.frame2, text='Recover password', command=lambda: self.loginhelpconfirm())
        self.button2 = Button(self.frame2, text='Go back',
                              command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                            login()))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.entry1.pack()
        self.button1.pack()
        self.button2.pack()

    def loginhelpconfirm(self):
        self.recoverusername = self.entry1.get()
        query = ("SELECT Date, username FROM passwordrecover WHERE username= %s")
        cursor.execute(query, (self.recoverusername,))
        if len(cursor.fetchall()) != 0:
            cursor.execute(query, (self.recoverusername,))
            for (Date, username) in cursor:
                print(datetime.date.today())
                print(Date)
                diff = to_integer(datetime.date.today()) - to_integer(Date)
                print(diff)
                if diff <= 1:
                    messagebox.showerror("Error", "Password was recovered already in the last 24 hours!")
                    self.frame1.pack_forget()
                    self.frame2.pack_forget()
                    self.loginhelp()
                    return

        query = ("SELECT email FROM credentials WHERE username= %s")

        cursor.execute(query, (self.recoverusername,))
        if len(cursor.fetchall()) == 0:
            messagebox.showerror("Error", "Wrong username!")
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.loginhelp()
        else:
            query = ("SELECT email FROM credentials WHERE username= %s")
            cursor.execute(query, (self.recoverusername,))
            for (email) in cursor:
                randomnumber = random.randint(0, 9999999)
                query = "INSERT INTO passwordrecover (Date, username, recoverycode) VALUES (%s, %s, %s)"
                cursor.execute(query, (datetime.date.today(), self.recoverusername, randomnumber))
                cnx.commit()
                me = ""
                you = ""
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Password Recover"
                msg['From'] = me
                msg['To'] = you
                text = "Hello %s!\nHow are you?\nSomeone requested your password to be recovered!\nHere is the recovery code you need: %s!\nGo to: %s\n \nHave a good one!" % (
                    email, randomnumber, link)
                html = """\
                    <html>
                      <head></head>
                      <body>
                        <p>Hello %s!<br>
                           How are you?<br>
                           Someone requested your password to be recovered!<br>
                           Here is the recovery code you need: %s<br>
                           Go to: %s<br>

                           Have a good one!<br>
                        </p>
                      </body>
                    </html>
                    """ % (email, randomnumber, link)

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')
                msg.attach(part1)
                msg.attach(part2)
                try:
                    server.sendmail(me, you, msg.as_string())
                    server.quit()
                    messagebox.showinfo("Sucess", "An email was sent with instructions on how to recover your password")
                except smtplib.SMTPException:
                    messagebox.showerror("Error!", "An error occurred sending this email, that's all we know.")
                    self.frame1.pack_forget()
                    self.frame2.pack_forget()
                    self.loginhelp()

    def loginsection(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.label1 = Label(self.frame1, text='Hello ' + inputusername + '!')
        self.button1 = Button(self.frame2, text='Change password', command=lambda: login.changepassword(self))
        self.button2 = Button(self.frame2, text='Logout', command=lambda: login.logout(self))
        self.button3 = Button(self.frame2, text='Delete', command=lambda: login.delete(self))
        self.button4 = Button(self.frame2, text='Two-Step Authentication', command=lambda: login.twostepauth(self))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()

    def changepassword(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.entry3 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Old Password:')
        self.label2 = Label(self.frame2, text='New Password:')
        self.label3 = Label(self.frame2, text='Re-Enter New Password:')
        self.button1 = Button(self.frame2, text='Change password', command=lambda: self.changepasswordconfirm())
        self.button2 = Button(self.frame2, text='Go back',
                              command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                            login.loginsection(self)))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.button1.pack()
        self.button2.pack()

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
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.label1 = Label(self.frame1, text='Enter your password:')
        self.entry1 = Entry(self.frame2)
        self.button1 = Button(self.frame2, text='Delete!', command=lambda: login.deleteconfirm(self))
        self.button2 = Button(self.frame2, text='Go back',
                              command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                            login.loginsection(self)))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.entry1.pack()
        self.button1.pack()
        self.button2.pack()

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

    def twostepauth(self):
        query = ("SELECT twostepauth FROM credentials WHERE username= %s")
        self.CheckVar1 = IntVar(root)
        cursor.execute(query, (inputusername,))
        for (twostepauth) in cursor:
            if '1' in twostepauth:
                global authstatus
                authstatus = 1
                self.CheckVar1.set(1)
            elif '0' in twostepauth:
                self.CheckVar1.set(0)
            else:
                messagebox.showerror("Error", "Your account does not support twostepauthentication")
                self.loginsection()
                return
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.frame1 = Frame(root)
            self.frame2 = Frame(root)
            self.label1 = Label(self.frame1, text='Enable/Disable Two-Step Authentication')
            self.checkbox1 = Checkbutton(self.frame2, variable=self.CheckVar1)
            self.button1 = Button(self.frame2, text='Go back',
                                  command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                                login.loginsection(self)))
            self.frame1.pack()
            self.frame2.pack()
            self.label1.pack()
            self.checkbox1.pack()
            self.button1.pack()

            def callback(*args):
                query = ("UPDATE credentials SET twostepauth= %s WHERE username= %s")
                if not self.CheckVar1.get():
                    cursor.execute(query, ('0', inputusername,))
                elif self.CheckVar1.get():
                    cursor.execute(query, ('1', inputusername,))
                cnx.commit()

            self.CheckVar1.trace("w", callback)


class register():
    def __init__(self):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.entry1 = Entry(self.frame1)
        self.entry2 = Entry(self.frame2)
        self.entry3 = Entry(self.frame2)
        self.entry4 = Entry(self.frame2)
        self.entry5 = Entry(self.frame2)
        self.label1 = Label(self.frame1, text='Username:')
        self.label2 = Label(self.frame2, text='Password:')
        self.label3 = Label(self.frame2, text='Re-Enter Password:')
        self.label4 = Label(self.frame2, text='E-Mail:')
        self.label5 = Label(self.frame2, text='Phone Number:')
        self.button1 = Button(self.frame2, text='Register', command=lambda: self.registerconfirm())
        self.button2 = Button(self.frame2, text='Go back',
                              command=lambda: combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(),
                                                            initialscreen()))
        self.frame1.pack()
        self.frame2.pack()
        self.label1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.label4.pack()
        self.entry4.pack()
        self.label5.pack()
        self.entry5.pack()
        self.button1.pack()
        self.button2.pack()

    def registerconfirm(self):
        query = ("SELECT * FROM credentials "
                 "WHERE username= %s OR email= %s OR phonenumber= %s")
        desiredusername = self.entry1.get()
        desiredpassword = self.entry2.get()
        desiredpassword2 = self.entry3.get()
        email = self.entry4.get()
        phone_number = self.entry5.get()

        if not EMAIL_REGEX.match(email):
            messagebox.showerror("Invalid Email", "The email you entered is invalid!")
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            register()
        else:
            cursor.execute(query, (desiredusername, email, phone_number,))
            if len(cursor.fetchall()) == 0:
                if desiredpassword2 == desiredpassword:
                    add_credential = ("INSERT INTO credentials "
                                      "(username, created, email, phonenumber, iterations, salt, hash) "
                                      "VALUES (%s, %s, %s, %s, '200000', %s, %s)")
                    add_credential_auth = ("INSERT INTO credentials "
                                           "(username, created, email, twostepauth, phonenumber, iterations, salt, hash) "
                                           "VALUES (%s, %s, %s, '0', %s, '200000', %s, %s)")
                    if use_two_step_authentication == 'true':
                        salt = bcrypt.gensalt()
                        hashedpassword = pbkdf2_sha256.encrypt(desiredpassword, rounds=200000, salt=salt)
                        cursor.execute(add_credential_auth, (
                            desiredusername, str(datetime.date.today()), email, phone_number, salt, hashedpassword))
                        cnx.commit()
                        messagebox.showinfo("Sucess!", "Account Registered!")
                        root.quit()
                        cursor.close()
                        cnx.close()
                    elif use_two_step_authentication == 'false':
                        salt = bcrypt.gensalt()
                        hashedpassword = pbkdf2_sha256.encrypt(desiredpassword, rounds=200000, salt=salt)
                        cursor.execute(add_credential, (
                            desiredusername, str(datetime.date.today()), email, phone_number, salt, hashedpassword))
                        cnx.commit()
                        messagebox.showinfo("Sucess!", "Account Registered!")
                        combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(), initialscreen())
                    else:
                        salt = bcrypt.gensalt()
                        hashedpassword = pbkdf2_sha256.encrypt(desiredpassword, rounds=200000, salt=salt)
                        cursor.execute(add_credential, (
                            desiredusername, str(datetime.date.today()), email, phone_number, salt, hashedpassword))
                        cnx.commit()
                        messagebox.showinfo("Sucess!", "Account Registered!")
                        messagebox.showwarning("Warning",
                                               "Variable misconfigured in source file - Variable: use_two_step_authentication")
                        combine_funcs(self.frame1.pack_forget(), self.frame2.pack_forget(), initialscreen())
                else:
                    messagebox.showerror("Password don't match!", "The password do not match!")
                    self.frame1.pack_forget()
                    self.frame2.pack_forget()
                    register()
            else:
                messagebox.showerror("Error", "This username/email/phone number is taken!")
                self.frame1.pack_forget()
                self.frame2.pack_forget()
                register()


def initialscreen():
    root.geometry('500x400')
    root.title('Login System')
    frame1 = Frame(root)
    frame2 = Frame(root)
    label1 = Label(frame1, text='Welcome to the login program!', font=5)
    button1 = Button(frame2, text='Login',
                     command=lambda: combine_funcs(frame1.pack_forget(), frame2.pack_forget(), login()))
    button2 = Button(frame2, text='Register',
                     command=lambda: combine_funcs(frame1.pack_forget(), frame2.pack_forget(), register()))
    frame1.pack()
    frame2.pack()
    label1.pack()
    button1.pack()
    button2.pack()
    root.mainloop()


root = Tk()
initialscreen()
