import sqlite3
from typing import Tuple



class queries:
    def __init__(self):
        self.con=sqlite3.connect("data/invmanage.db")
        self.cur=self.con.cursor()

        
    #table parameter used to specify which table to check
    def check_email_exists(self,email:str,table:str)->bool:
        self.cur.execute("SELECT * FROM {} WHERE email=?".format(table),(email,))
        result = self.cur.fetchone()
        if result is None:
            return(False)
        else:
            return(True)
    
    #takes in salted + hashed pw and checks with database
    def check_password(self,password:str,table:str,email:str):
        self.cur.execute("SELECT password FROM {} WHERE email=?".format(table),(email,))
        db_pw = self.cur.fetchone()[0]
        if db_pw == password:
            return True
        else:
            return False

    def get_salt(self,email:str,table:str)->str:
        params=(table,email)
        self.cur.execute("SELECT salt FROM {} WHERE email = ?".format(table),(email,))
        return(self.cur.fetchone()[0])
    
    def get_row_by_email(self,email:str,table:str)-> Tuple:
        self.cur.execute("SELECT * FROM {} WHERE email=?".format(table),(email,))
        return(self.cur.fetchone())
    def write_new_cust_user(self,uid:str,name:str,email:str,phone_num:str,address:str,password:str,salt:str):
        params = (uid,name,email,phone_num,address,password,salt)
        self.cur.execute("INSERT into customer (uid,name,email,phone_num,address,password,salt) VALUES(?,?,?,?,?,?,?)",params)
        self.con.commit()
    #overwrite records, UID is primary key for all tables. arguments field_name,field_value can be tuples if updating multiple fields.
    def overwrite_field(self,field_name,table:str,field_value,uid:str):
        #for one field only
        if len(field_value) == 1:
            params = (field_value,uid)
            self.cur.execute("""
            UPDATE {}
            SET {} = ?
            WHERE uid = ?
            """.format(table,field_name),params)
            self.con.commit()
        #for more than one field:
        else:
            params = field_value + (uid,)
            format_str_tuple = (table,)+field_name
            query_string = "UPDATE {} SET {} =?"
            for i in range(len(field_value)-1):
                query_string += ", {} =?"
            query_string += "WHERE uid =?"
            self.cur.execute(query_string.format(*format_str_tuple),params)
            self.con.commit()


        


#call this function to instantiate query object for other modules to perform queries
def create_query_obj():
    global query_obj
    query_obj = queries()

