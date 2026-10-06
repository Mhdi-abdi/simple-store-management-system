from datetime import datetime
from typing import Optional

class Order:
    def __init__(self,
                order_id : Optional[int],
                customer_id:int,
                status:str,
                order_date:datetime,
                total_price:float):

        self.order_id = order_id
        self.customer_id = customer_id
        self.status = status
        self.order_date = order_date
        self.total_price = total_price