import sqlite3
from typing import Tuple

class InvalidArugments(Exception):
    def __init__(self,message="Invalid Argument was provided somewhere."):
        self.message = message



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
    #overwrite records, selects row(s) by id, if no id field is passed, defaults to "uid"
    def overwrite_field_id(self,field_name,table:str,field_value,uid:str,id_type = "uid"):
        #for one field only
        if len(field_value) == 1:
            params = (field_value,uid)
            self.cur.execute("""
            UPDATE {}
            SET {} = ?
            WHERE {} = ?
            """.format(table,field_name,id_type),params)
            self.con.commit()
        #for more than one field:
        else:
            params = field_value + (uid,)
            format_str_tuple = (table,)+field_name
            query_string = "UPDATE {} SET {} =?"
            for i in range(len(field_value)-1):
                query_string += ", {} =?"
            query_string += "WHERE {} =?"
            self.cur.execute(query_string.format(*format_str_tuple,id_type),params)
            self.con.commit()
    #field_name,field_values tuple even for singular case
    def new_row(self,table:str,field_values:Tuple):
        #case for rows with singular data
        if len(field_values) == 1:
            self.cur.execute("""INSERT INTO {},
                             VALUES (?)
                             """.format(table),field_values)
            
            
        else:
            #generate the query based on how many columns we are inserting into
            query_string = """INSERT INTO {},
            VALUES (?"""
            for i in range(len(field_values)-2):
                query_string += ",?"
            query_string += ",?)"
            self.cur.execute(query_string)
        self.con.commit()
    
    #update id_counter by 1 whenever a new product/order is created
    def update_id_counter(self,type:str):
        try:
            if type == "product":
                self.cur.execute("UPDATE id_counter SET product = product + 1")
            elif type == "order":
                self.cur.execute("UPDATE id_counter SET order = order + 1")
            else:
                raise InvalidArugments()
        except InvalidArugments:
            print("Invalid arguments were provided into update_id_counter")
    
    def get_id_counter(self,type:str) -> int:
        try:
            if type == "product":
                self.cur.execute("SELECT product FROM id_counter")
                return self.cur.fetchone()
                
            elif type == "order":
                self.cur.execute("SELECT order FROM id_counter")
                return self.cur.fetchone()
            else:
                raise InvalidArugments()
        except InvalidArugments:
            print("Invalid arguments were provided into update_id_counter")

            

        

        
            
        




        


#call this function to instantiate query object for other modules to perform queries
def create_query_obj():
    global query_obj
    query_obj = queries()

