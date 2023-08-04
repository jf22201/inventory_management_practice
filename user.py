import queries,menus
import secrets,hashlib,getpass,uuid,time
from typing import Dict,Tuple



class user:
    def __init__(self,name:str=None,email:str=None,uid:str=None):
        self.name = name
        self.email = email
        self.uid = uid
    def set_name(self,name)-> None:
        self.name = name
    def set_email(self,email) -> None:
        self.email = email
    def set_uid(self,uid) -> None:
        self.uid = uid
    

class customer(user):
    def __init__(self,name:str=None,email:str=None,uid:int=None,phone_num:int=None,address:str=None):
        super().__init__(name,email,uid)
        self.phone_num = phone_num
        self.address = address
        self.account_type = "customer"
        #basket is dictionary with keys: product id (pid) and values: dictionary with keys: price,quantity
        self.basket :Dict[str, Dict] = {}
    def basket_total(self)->float:
        if len(self.basket.values()) == 0:
            return(0.00)
        else:
            total = 0
            for product in self.basket.values():
                total =+ product["Price"] * product["Quantity"]
            return(total)   
    def set_address(self,address:str):
        self.address = address
    def set_phone_num(self,phone_num:str):
        self.phone_num = phone_num
    def update_info(self) -> None:
        resp_bool = True
        while resp_bool == True:
            print("Your current info on record is:\nName: {}, Email: {}, Phone Num: {}, Address: {}".format(self.name,self.email,self.phone_num,self.address))
            print("What would you like to update?\n1) Name\n2) Email\n3) Phone number \n4) Address\n5) Password\n6) Return to login menu")
            menu_resp = input("Please enter your selection here:")
            if menu_resp == "1":
                update_value = input("Enter your updated name here:")
                queries.query_obj.overwrite_field(field_name="name",table="customer",field_value=update_value,uid=self.uid)
                self.name = update_value
                print("Update successful!")
            elif menu_resp == "2":
                update_value = input("Enter your updated email here:")
                queries.query_obj.overwrite_field(field_name="email",table="customer",field_value=update_value,uid=self.uid)
                self.email = update_value
                print("Update successful!")
            elif menu_resp == "3":
                update_value = input("Enter your updated phone number here:")
                queries.query_obj.overwrite_field(field_name="phone_num",table="customer",field_value=update_value,uid=self.uid)
                self.phone_num = update_value
                print("Update successful!")
            elif menu_resp == "4":
                update_value = input("Enter your updated address here:")
                queries.query_obj.overwrite_field(field_name="address",table="customer",field_value=update_value,uid=self.uid)
                self.address = update_value
                print("Update successful!")
            elif menu_resp == "5":
                update_value = enter_and_check_pw()
                #generate a new salt for the updated password and hash the new password, pw:index 0, salt:index1.
                pass_tuple = pass_handle.gen_salt_hash(update_value)
                queries.query_obj.overwrite_field(field_name=("password","salt"),table="customer",field_value=pass_tuple,uid=self.uid)
                print("Update successful!")
                

            else:
                
                print("Sorry, your selection was not recognized.")
                time.sleep(2)


        



class manage(user):
    def __init__(self,name:str=None,email:str=None,uid:str=None):
        super().__init__(name,email,uid)
        self.account_type = "manage"
    def update_info(self):
        resp_bool = True
        while resp_bool == True:
            print("Your current info on record is:\nName: {}, Email: {}".format(self.name,self.email,self.phone_num,self.address))
            print("What would you like to update?\n1) Name\n2) Email\n3) Password\n4) Return to log on menu")
            menu_resp = input("Please enter your selection here:")
            if menu_resp == "1":
                update_value = input("Enter updated name here:")
            elif menu_resp == "2":
                update_value = input("Enter updated email here:")
            elif menu_resp == "3":
                update_value = enter_and_check_pw()
                pass_tuple = pass_handle.gen_salt_hash(update_value)
                queries.query_obj.overwrite_field(field_name=("password","salt"),table="manage",field_value=pass_tuple,uid=self.uid)
                print("Update successful!")
            elif menu_resp == "4":
                resp_bool = False
            else:
                print("Your selection wasn't recognized.")
                time.sleep(2)

            




class admin(manage):
    def __init__(self,name:str=None,email:str=None,uid:str=None):
        super().__init__(name,email,uid)
        self.account_type = "admin"


#takes password as a input and returns tuple containing: salted and hashed password as string, salt value in plaintext
class pass_handle:
    
    #adds salt to plaintext password and hashes then returns the result
    @staticmethod
    def salt_hash(password:str,salt:str)->str:
        salted_pw = password + salt
        hashed_pw = hashlib.sha256(salted_pw.encode()).hexdigest()
        return(hashed_pw)
        
    #generates a random salt and hashs with the password
    @staticmethod
    def gen_salt_hash(password:str) -> Tuple[str,str]:
        salt = secrets.token_hex(10)
        salted_pw = password+salt
        hashed_pw = hashlib.sha256(salted_pw.encode()).hexdigest()
        return((hashed_pw,salt))


#object used to log in to accounts
class login:
    def __init__(self,login_type:str):
        self.logged_in = False
        self.email = None
        self.password = None
        #login type contains string of which table to check for account in database
        self.login_type = login_type
    def return_user_obj(self,email:str)->user:
        #getting attributes of user from database
        info_tuple:Tuple = queries.query_obj.get_row_by_email(email=self.email,table=self.login_type)
        #creating user objects using attributes
        #customer active user
        if self.login_type == "customer":
            return customer(uid=info_tuple[0],name=info_tuple[1],email=info_tuple[2],phone_num=info_tuple[3],address=info_tuple[4])
            
        #admin active user
        elif self.login_type == "manage" and info_tuple[5] == 1:
            return admin(uid=info_tuple[0],name=info_tuple[1],email=info_tuple[3])
        #standard management active user
        else:
           return manage(uid=info_tuple[0],name=info_tuple[1],email=info_tuple[3])
          
    def log_user_in(self):
        while True:
            self.email:str = input("Enter your account email here:")
            if queries.query_obj.check_email_exists(email = self.email,table = self.login_type):
                break
            else:
                print("Email is not registered on system.")
        salt:str = queries.query_obj.get_salt(email=self.email,table=self.login_type)
        while True:
            self.password = getpass.getpass("Enter password:")
            hashed_pw:str = pass_handle.salt_hash(password=self.password,salt=salt)
            if queries.query_obj.check_password(password=hashed_pw,email=self.email,table=self.login_type):
                print("You have successfully logged in.")
                break
            else:
                print("The password was not correct.")
        return self.return_user_obj(self.email)
        
def create_cust_account():
    while True:
        email = input("Please enter your email here:")
        if queries.query_obj.check_email_exists(email,table="customer"):
            print("This email already exists in our system")
            print("\n Would you like to: \n 1) Try again\n 2) Return to main menu")
            response = input("Please enter your choice here: ")
            if response == "1":
                pass
            elif response == "2":
                return
            else:
                print("Invalid response please try again.")
        else:
            password = enter_and_check_pw()
                #call method to salt and hash password, returns tuple (hashed_pw,salt)
            pw_salt_tuple = pass_handle.gen_salt_hash(password)
            #randomly generate a UUID to identify users
            uid = uuid.uuid4().hex
            name = input("Please enter your name:")
            address = input("Please enter your address:")
            phone_num = input("Please enter your phone number:")
            queries.query_obj.write_new_cust_user(uid,name,email,phone_num,address,pw_salt_tuple[0],pw_salt_tuple[1])
            print("Your account has successfully been created.")
            break
    # def change_user_info()-> None:
    #     info_list = [menus.active_user.name,menus.active_user.email]
    #     if menus.active_user.account_type == "customer":
    #         info_list.append(menus.active_user.phone_num)
    #         info_list.append(menus.active_user.address)
    #         print("Your current information on record is:\nName: {}\nEmail: {}\nPhone number: {}\nAddress: {}\n").format(info_list[0],info_list[1],info_list[2],info_list[3])


# function to for password input and verification 
def enter_and_check_pw() -> str:
    while True:
                password = getpass.getpass("Enter your password")
                confirm_password = getpass.getpass("Re-enter your password")
                if password == confirm_password:
                    break
                else:
                    print("The entered passwords did not match.")
    return password




                


        
        
    




        

    



        
        

        

        
    

    