from datetime import datetime

class Order:
    def __init__(self,
                customer_id:int,
                status:str,
                order_date:datetime,
                total_price:float):

        self.customer_id = customer_id
        self.status = status
        self.order_date = order_date
        self.total_price = total_price