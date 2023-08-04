from typing import Dict 
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

