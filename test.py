import mysql.connector
import datetime

cnx = mysql.connector.connect(user='root', password='01122rfg@', host='127.0.0.1', database='logininfo')
cursor = cnx.cursor()

def login():
    print('Enter your username:')
    global inputusername
    inputusername = input()
    print('Enter your password:')
    inputpassword = input()

    query = ("SELECT * FROM credentials "
             "WHERE username= %s AND password= %s")

    cursor.execute(query, (inputusername, inputpassword))

    if len(cursor.fetchall()) == 0:
        print('Wrong username/password combination!')
    else:
        print('Login Sucessfull!')
        inputpassword = 'NULL'
        loginsection()

def register():
    print('Enter desired username:')
    desiredusername = input()

    query = ("SELECT * FROM credentials "
             "WHERE username= %s")

    cursor.execute(query, (desiredusername, ))
    if len(cursor.fetchall()) == 0:
        print('Enter desired password:')
        desiredpassword = input()

        add_credential = ("INSERT INTO credentials "
                          "(username, password, created) "
                          "VALUES (%s, %s, %s)")
        cursor.execute(add_credential, (desiredusername, desiredpassword, str(datetime.date.today())))
        cnx.commit()

        cursor.close()
        cnx.close()
    else:
        print('This username is alredy taken!')
        register()

def loginsection():
    print('Hello', inputusername, '!')
    print('Actions - Change password, Logout, Delete')
    action2 = input()
    if action2 == 'Change password':
        oldpassword = input('Enter your old password: ')
        newpassword = input('Enter your new password: ')
        newpassword2 = input('Confirm your new password: ')

        query = ("SELECT * FROM credentials WHERE username= %s AND password= %s;")

        cursor.execute(query, (inputusername, oldpassword))
        if len(cursor.fetchall()) == 0:
            print('Wrong password!')
            loginsection()
        else:
            if newpassword == newpassword2:
                update_password = ("UPDATE credentials SET password = %s WHERE username = %s")
                cursor.execute(update_password, (newpassword, inputusername))
                cnx.commit()
                print('Password Altered!')
                loginsection()
            else:
                print('Passwords do not match!')
                loginsection()
    elif action2 == 'Logout':
        cursor.close()
        cnx.close()
    elif action2 == 'Delete':
        password = input('Enter your password: ')
        query = ("SELECT * FROM credentials WHERE username= %s AND password= %s;")

        cursor.execute(query, (inputusername, password))
        if len(cursor.fetchall()) == 0:
            print('Wrong password!')
            loginsection()
        else:
            delete_account = ("DELETE FROM credentials WHERE username= %s")
            confirm = input('Are you sure? (Yes or No): ')
            if confirm == 'Yes':
                cursor.execute(delete_account, (inputusername, ))
                print('Account deleted!')
                cnx.commit()
                cursor.close()
                cnx.close()
print('Welcome to the login program!')
print('Register or Login?')
action = input()
if action == 'Register':
    register()
elif action == 'Login':
    login()
