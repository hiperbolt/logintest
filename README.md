# logintest
I tried using mysql with python for the first time. It took a day, but I did it, and self-taught.

## Features:
Two-Factor Authentication using the Twilio API.
Password Recovery System
Infinite Accounts
E-Mail Validity Check using REGEX.

## test.py
A Non-GUI version of the program. Served as the bones behind the gui version.

## guitest.py
The GUI / Full version of this concept program. ( Well, concept for me at least, a python learner :p )

## MySQL Side of things.
Im using a local-hosted MariaDB installation on Arch Linux with a DB called logininfo, using the table "credentials" that holds the values: username (varchar(20)), email (varchar(60)), password (varchar(20)), created (date), twostepauth (varchar(20), phonenumber (varchar(20)).

I'll post a tutorial on the wiki on how to set this up.

## How to install / use:
I'll post a tutorial on the wiki of this program on how to use it, if you want for example a base to start off, on a login program.
I am also planning to do a walkthrough of my messy code.
