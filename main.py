#user created modules
import queries,user,product,tablecreation,menus
#python standard modules
import os
#create tables if database doesn't exist
if  os.path.exists("data/invmanage.db") == False:
    print("database not found, will create database and tables.")
    #create tablecreation object to access table creation methods
    tc = tablecreation.table_creator()
    tc.create_cust_table()
    tc.create_manage_table()
            #commit changes
    print("database created, please enter details for admin account")
    tc.create_admin()
    tc.commit()
    tc.close()
    print("Account created successfully.")

#create query object to allow all modules to perform queries
queries.create_query_obj()
menus.main_menu()





    
    





        

    
