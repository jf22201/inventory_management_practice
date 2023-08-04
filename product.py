from typing import Dict 
class Product:
    def __init__(self,name:str=None,desc:str=None,price:float=None,pid:int=None,instock:int=None):
        self.__name = name
        self.desc = desc
        self.__price = price
        self.__pid =  pid
        self.__instock = instock
    def get_stock(self) -> int:
        return(self.__instock)
    def get_name(self) -> str:
        return(self.__name)
    def get_desc(self) -> str:
        return(self.__desc)
    def get_id(self) -> int:
        return(self.__id)
    def set_stock(self,stock) -> None:
        self.__instock = stock
    def set_desc(self,desc) -> None:
        self.__desc = desc
    def set_price(self,price) -> None:
        self.__price = price
    def set_id(self,id) -> None:
        self.__id = id


#outer dictionary key is product by pid, outer value is dictionary containing properties of each product
#product_list: Dict[str:Dict[str:str]] = {}
