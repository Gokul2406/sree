import sys
import mysql.connector as m
from datetime import date
from cryptography.fernet import Fernet

mycon=m.connect(host='localhost',user='root',passwd="root",database='BANK')
cursor=mycon.cursor(buffered=True)



def setup():
    cursor.execute('CREATE TABLE if not exists USERS(USERNAME varchar(20),ACCOUNT_NO int primary key,DATE_ENTRY date,BALANCE int,PASSWORD varchar(100))')
    cursor.execute('CREATE TABLE if not exists TRANSACTIONS(FROM_USER varchar(20),TO_USER varchar(20),DATE date,AMOUNT int)')
    mycon.commit()
    cursor.execute("create table if not exists MISC(encr_key varchar(500))")



    key = Fernet.generate_key()

    cursor.execute(f"INSERT INTO MISC VALUES ('{key.decode()}')")
    mycon.commit()
def login(username):
    fetch_key = "select * from MISC"

    cursor.execute(fetch_key)

    res = cursor.fetchall()

    for i in res:
        for key in i:
            fernet = Fernet(key.encode())
            
            
            entered_password = input("Enter password: ")
        

            cursor.execute(f"select PASSWORD from USERS where USERNAME = '{username}'")
            res = cursor.fetchall()
            
            for record in res:
                for password in record:
                    decr_password = fernet.decrypt(password.encode())
                    

                    if decr_password.decode() == entered_password:
                        return True
                    else:
                        return False
                



def add_ac():
    user_name=input("Enter your name")
    ac_no=int(input("Enter the account number"))
    balance=int(input("Enter the account balance"))
    date1=date.today()    
    password = input("Enter password: ")

    cursor.execute("select * from MISC")
    res = cursor.fetchall()

    for i in res:
        for key in i:
            fernet = Fernet(key.encode())
            password = fernet.encrypt(password.encode())


    cursor.execute("INSERT INTO USERS VALUES('{}',{},'{}',{}, '{}');".format(user_name,ac_no,date1,balance, password.decode()))
    mycon.commit()


def close_ac():
    user_name=input("Enter the username")
    ac_no=input("Enter the account No")
    cursor.execute("DELETE FROM USERS WHERE USERNAME='{}' and ACCOUNT_NO={}".format(user_name,ac_no))
def do_transactions(username):
    to_user=input("Enter the user you want to transfer money")
    acn=input("Enter account no:")
    amount=int(input("Enter the amount"))
    cursor.execute("UPDATE USERS SET BALANCE=BALANCE-{} WHERE USERNAME='{}'".format(amount,username))
    cursor.execute("UPDATE USERS SET BALANCE=BALANCE+{} WHERE USERNAME='{}' AND ACCOUNT_NO={} ".format(amount,to_user,acn))
    cursor.execute("INSERT INTO TRANSACTIONS VALUES('{}','{}','{}',{})".format(username,to_user,date.today(),amount))
    mycon.commit()

def view_account(username):
     cursor.execute("SELECT * FROM USERS where USERNAME = '{}'".format(username))
     row=cursor.fetchone()

     if row[0]==username:
         print('Username:\t',row[0])
         print('Account NO:\t',row[1])
         print("Balance:\t",row[3])
     else:
         print("Incorrect password or user does not exist")
def view_transactions():
    cursor.execute("SELECT * FROM TRANSACTIONS")
    l=cursor.fetchall()
    print("FROM\tTO\tDATE\tAMOUNT\t")
    for i in l:
        print(i[0],i[1],i[2],i[3])
        
        

#add_ac()
#setup()

while True:
    print("""WELCOME TO BANK 
            1) Login
            2) Add account
            3) Exit
     """)
    ch = int(input("Enter choice: "))
    if ch == 1:
        username = input("Enter username: ")
        res = login(username)
        if res == False:
            sys.exit(0)
        else:
            ask=input("Are you admin[y,n]")
            if ask=='y':
                res2=login()
                if res2==False:
                    print("You are not admin") 
                    sys.exit(0)
                else:
                    loop=True
                    while loop:
                        print("""WELCOME TO ADMIN PAGE 
                                  1.ADD ACCOUNT 
                                  2.CLOSE ACCOUNT 
                                  3.VIEW ALL THE USERS
                                  4.VIEW ALL THE TRANSACTIONS
                                  5.EXIT             """)   
                                        
                        w=input("Enter choice")
                        if w=='1':
                            add_ac()
                        elif w=='2':
                            close_ac()
                        elif w=='3':
                            pass
                        elif w=='4':
                             view_transactions()
                        elif w=='5':
                            loop=False
                        else:
                            print("Enter correct choice")
            elif ask=='n':
                loop2=True
                while loop2:
                    print("""WELCOME TO USER PAGE
                                1.VIEW ACCOUNT 
                                2.TRANSFER MONEY
                                3.EXIT""")
                    m=input("Enter choice")
                    if m=='1':
                        view_account(username) 
                    elif m=='2':
                        do_transactions(username)
                    elif m=='3':
                        loop2=False
                    else:
                        print("Enter correct choice")

mycon.close()