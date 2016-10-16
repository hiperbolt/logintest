import re
import sys
import os
import mysql.connector
from passlib.hash import pbkdf2_sha256
import bcrypt
from subprocess import call

cnx = mysql.connector.connect(user='', password='', host='',
                              database='logininfo')  # MySQL Connector Information
cursor = cnx.cursor()

def main():
	recoverycode = str(sys.argv[1])
        query = "SELECT username FROM passwordrecover WHERE recoverycode = %s"
        cursor.execute(query, (recoverycode,))
        for (username) in cursor:
                stringusername = str(username)
                fixedusername = re.findall(r"'(.*?)'",stringusername)
                salt = bcrypt.gensalt()
                desiredpassword = str(sys.argv[2])
                hashedpassword = pbkdf2_sha256.encrypt(desiredpassword, rounds=200000, salt=salt)
                query = "UPDATE credentials SET salt = %s, hash = %s WHERE username = %s"
                cursor.execute(query, (salt, hashedpassword, fixedusername[0]))
                query = "UPDATE passwordrecover SET recoverycode = NULL WHERE recoverycode = %s"
                cursor.execute(query, (recoverycode,))
                cnx.commit()

main()
