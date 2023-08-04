import user
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
        
    else:
        print("You are logged in as {}".format(active_user.name))