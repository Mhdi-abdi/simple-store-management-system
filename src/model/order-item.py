class OrderItem:
    def __init__(self,
                order_id:int,
                product_id:int,
                unit_price:float,
                quantity:int):

        self.order_id = order_id
        self.product_id = product_id
        self.unit_price = unit_price
        self.quantity = quantity