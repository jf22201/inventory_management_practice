import sqlite3,getpass,uuid,user
from typing import Tuple

#interface for creating tables in case they do not exist
class table_creator:
    def __init__(self):
        self.conn_tc = sqlite3.connect('data/invmanage.db')
        self.cur_tc = self.conn_tc.cursor()
        


    def create_cust_table(self)->None:
        

        self.cur_tc.execute("""
            CREATE TABLE customer(
            uid INTEGER,
            name TEXT,
            email TEXT,
            phone_num TEXT,
            address TEXT,
            password TEXT,
            salt TEXT
            )

""")
#create management account table
    def create_manage_table(self)->None:
        self.cur_tc.execute("""
CREATE TABLE manage(
            uid TEXT,
            name TEXT,
            email TEXT,
            password TEXT,
            salt TEXT,
            is_admin INTEGER
            )
            """)
    def create_admin(self):
        email:str = input("Email:")
        while True:
            password:str = getpass.getpass("password:")
            confirm_pass:str = getpass.getpass("verify password")
            if password == confirm_pass:
                break
            else:
                print("The entered passwords were not the same, please try again.")
        name:str =input("Enter your full name:")
        userid:str = uuid.uuid4().hex
        #call password hashing+salting function
        hashpw_salt:Tuple[str,str] = user.pass_handle.gen_salt_hash(password)
        params = (userid,name,email,hashpw_salt[0],hashpw_salt[1],1)
        self.cur_tc.execute("""
                            INSERT INTO manage (uid,name,email,password,salt,is_admin)
                            VALUES (?,?,?,?,?,?)
                            """,params)



        
        
    #commit method to commit changes to DB
    def commit(self)->None:
        self.conn_tc.commit()
    def close(self)->None:
        self.conn_tc.close()



