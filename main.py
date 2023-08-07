#user created modules
import queries,user,product,tablecreation,menus
#python standard modules
import os
#create tables if database doesn't exist
if  os.path.exists("data/invmanage.db") == False:
    print("database not found, will create database and tables.")
    #create tablecreation object to access table creation methods
    tc = tablecreation.table_creator()
    #run first time setup method to create all tables.
    tc.first_time_setup()

#create query object to allow all modules to perform queries
queries.create_query_obj()
menus.main_menu()





    
    





        

    
