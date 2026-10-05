from typing import Optional
class Customer:
    def __init__(self,
                customer_id : Optional[int],
                first_name:str,
                last_name :str,
                email:str, 
                phone:str = None,
                city:str = None, 
                country:str = None, 
                postal_code:str = None):

        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.city = city
        self.country = country
        self.postal_code = postal_code