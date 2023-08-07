from typing import Dict 
import queries
import time
class Product:
    def __init__(self,name:str=None,desc:str=None,price:float=None,pid:int=None,stock:int=None):
        self.name = name
        self.desc = desc
        self.price = price
        self.productid =  pid
        self.stock = stock
 

#outer dictionary key is product by pid, outer value is dictionary containing properties of each product
#product_list: Dict[str:Dict[str:str]] = {}

class product_list:
    def __init__(self):
        self.list = []
    #INCOMPLETE
    def read_from_db(self)->None:
        #fetch product info from db and store in prod_list
        db_list = queries.query_obj.get_all_prod()
        for tuple in db_list:
            self.list.append(Product(name=tuple[1],desc=tuple[3],price=tuple[2],pid=tuple[0],stock=tuple[4]))
    #method to view products in a page like format
    def view_prods(self,page:int) ->None:
        if len(self.list) <= 10:
            for count,product in enumerate(self.list):
                print(str(count+1) + ") Name:" + product.name + "id: " + product.id)
        else:
            num_pages = ((len(self.list) - 1)// 10)+1
            last_page_len = len(self.list) % 10
            if page == num_pages:
                start_ind = (num_pages - 1) * 10
                end_ind = start_ind + last_page_len + 1
                for count,product in enumerate(self.list[start_ind:end_ind]):
                    print(str(count+1) + ") Name:" + product.name + "id: " + product.id)
                
            else:
                start_ind = (page - 1) * 10
                end_ind = (page * 10)
                for count,product in enumerate(self.list[start_ind:end_ind]):
                    print(str(count+1) + ") Name:" + product.name + "id: " + product.id)
    
    def prod_menu_manage(self) -> None:
        self.view_prods(1)











    

#call this function to initalize an instance of product_list for all modules to use
def init_product_list() -> product_list:
    global prod_list
    prod_list = product_list()
