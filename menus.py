from typing import Tuple
import user,product
import time
def main_menu():
    while True:
        
        #initialize active user as none
        global active_user
        active_user = None
        print("1) Customer Login\n2) Management login\n3) Create new customer account")
        response_var = input("Please enter your selection here: ")
        #create login object to login, different login method depending on customer/manage
        #if login successful active_user is set to customer,manage or admin object depending on the user.login object
        if response_var == "1":
            login_obj = user.login("customer")
            active_user = login_obj.log_user_in()
        elif response_var == "2":
            login_obj = user.login("manage")
            active_user = login_obj.log_user_in()
        elif response_var == "3":
            user.create_cust_account()
        else:
            print("Invalid choice, please choose again.")
            
        if not active_user == None:
            logged_in_menu()


def logged_in_menu():
    product.init_product_list()
    if active_user.account_type == "customer":
        print("You are logged in as: {}".format(active_user.name))
        #Keep user in selection menu until valid selection made
        resp_bool : bool = True
        while resp_bool == True:
            print("\n1) Check products\n2) Place order\n3) Change account info\n4) Log out")
            logged_in_resp:str = input("Please enter your selection here: ")
            if logged_in_resp == "1":
                pass

            elif logged_in_resp == "2":
                pass
    
            elif logged_in_resp == "3":
                active_user.update_info()
            elif logged_in_resp =="4":
                resp_bool == False
                print("You have been logged out.")
            else:
                print("Sorry that was an invalid input, please try again.")
        


    elif active_user.account_type == "admin":
        print("You are logged in as: {}".format(active_user.name))
        resp_bool : bool = True
        while resp_bool == True:
            print("\n1) Manage products\n2) Manage orders\n3) Change account info\n4) Manage users\n 5) Log out")
            logged_in_resp:str = input("Please enter your selection here: ")
            if logged_in_resp == "1":
                active_user.manage_products()
                

            elif logged_in_resp == "2":
                pass
    
            elif logged_in_resp == "3":
                active_user.update_info()
            elif logged_in_resp =="5":
                resp_bool == False
                print("You have been logged out.")
            else:
                print("Sorry that was an invalid input, please try again.")
        

        
    else:
        print("You are logged in as {}".format(active_user.name))

class SelectionMenu:
    #display_tuple is tuple of options to show on menu(str), selections_tuple are the possible inputs for the user to select their desired option
    def __init__(self,display_tuple:Tuple[str],selections_tuple:Tuple[str]):
        try:
            self.display_tuple = display_tuple
            self.selections_tuple = selections_tuple
            self.length = len(display_tuple)
            if self.length != len(selections_tuple):
                raise Exception 
        
        except Exception as e:
            print("The length of the arguments do not match.")
    
    #displays menu and takes user input then returns the input.
    def show_menu_return_input(self)->str:
        if self.length == 1:
            while True:
                print(self.selections_tuple[0] + ") " + self.display_tuple[0]+"\n")
                selection = input("Type your input here: ")
                if selection not in self.selections_tuple:
                    print("Invalid input, please try again.")
                    time.sleep(2)
                else:
                    return(selection)
        else:
            while True:
                for selection,display in zip(self.selections_tuple,self.display_tuple):
                    print(selection+") " + display)
                selection = input("Type your input here")
                if selection not in self.selections_tuple:
                     print("Invalid input, please try again.")
                     time.sleep(2)
                else:
                    return(selection)
                    
            
        

        
