from typing import Optional

class Product:
    def __init__(self,
                product_id : Optional[int],
                product_name:str,
                price:float,
                stock_quantity:int,
                description:str = None,
                is_active:bool = True):

        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.stock_quantity = stock_quantity
        self.description = description
        self.is_active = is_active