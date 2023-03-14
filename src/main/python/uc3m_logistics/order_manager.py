"""Module """
import json
import os

from .order_management_exception import OrderManagementException
from .order_request import OrderRequest

class OrderManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        store_path = "../stores/"
        current_path = os.path.dirname(__file__)
        self.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")
        print("Order request store: ", self.__order_request_json_store)

    @staticmethod
    def validate_ean13(cls, ean13_code):
        """RETURNs TRUE IF THE CODE RECEIVED IS A VALID EAN13,
        OR FALSE IN OTHER CASE"""
        return ean13_code

    def validate_order_type(cls, order_type):

        if not isinstance(order_type, str):
            raise OrderManagementException("Invalid order type: not a string")
        if order_type not in ["Regular", "Premium"]:
            return order_type ## TODO double check
    def validate_address(cls, address):
        return address

    def validate_phone_number(cls, phone_number):
        return phone_number

    def validate_zip_code(cls, zip_code:str):
        if not isinstance(zip_code, str):
            raise OrderManagementException("Invalid zip code: not a string")
        return zip_code

    def register_order(self, product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: int) -> str:
        self.validate_ean13(product_id)
        self.validate_order_type(order_type)
        self.validate_address(address)
        self.validate_phone_number(phone_number)
        self.validate_zip_code(zip_code)
        order_request = OrderRequest(product_id, order_type, address, phone_number,zip_code)
        with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            data = json.load(file)
            data.append(order_request.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
        return order_request.order_id