import mysql.connector as c
mycon=c.connect(host="localhost",user="root",passwd="anjana",database="psc_registration")
mycursor=mycon.cursor()
while True:
    print("1.signup 2. login 3.exit")
    ch=int(input("enter your choice"))
    if ch==1:
        print("enter your details")
       
           
        user=input("enter user id")
        pas=input("enter password")
        name=input("enter your name")
        age=int(input("enter your age"))
        

        mycursor.execute("insert into registration values ('{}','{}','{}',{})".format(user,pas,name,age))
        mycon.commit()
        print("registered ")
        
    elif ch ==2:
        chh=int(input("enter choice 1.view details 2.edit details 3.exit"))
        if chh==1:
            user=input("enter user id")
            pas=input("enter password")
            
            s=mycursor.execute("select * from registration where user like'{}' and password like'{}'".format(user,pas))
            
            reg=mycursor.fetchall()
            if reg==[]:
                print("incorrect user name or password ")
            
            else:
                headers=[x[0] for x in mycursor.description]
            
                        
                print("                 ",headers,"                           ")
        
                for i in reg:
                    print("                 ",i,"                             ")
        
        
        
         if chh==2:
             print("what do u 
            
                
        
            pass

mycursor.close()
mycon.close()
    
