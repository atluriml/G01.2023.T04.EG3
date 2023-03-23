"""Module"""
import json
import os
from barcode import EAN13
from .order_management_exception import OrderManagementException
from .order_request import OrderRequest

class OrderManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        store_path = "../stores/"
        current_path = os.path.dirname(__file__)
        self.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")
        self.__order_manager_json_store = os.path.join(current_path, store_path, "order_manager.json")
        self.__order_shipping_json_store = os.path.join(current_path, store_path, "order_shipping.json")
        print("Order request store: ", self.__order_request_json_store)
        print("Order manager store: ", self.__order_manager_json_store)
        print("Order shipping store: ", self.__order_shipping_json_store)

        try:
            if not os.path.exists(self.__order_request_json_store):
                with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception: # finish
            raise OrderManagementException("Could create/find order_request.json") from exception

        try:
            if not os.path.exists(self.__order_manager_json_store):
                with open(self.__order_manager_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception: # finish
            raise OrderManagementException("Could create/find order_manager.json") from exception

        try:
            if not os.path.exists(self.__order_shipping_json_store):
                with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception: # finish
            raise OrderManagementException("Could create/find order_shipping.json") from exception

    @staticmethod
    def validate_ean13(cls, ean13_code): #TODO ask about cls
        """RETURNS TRUE IF THE CODE RECEIVED IS A VALID EAN13,
        OR FALSE IN OTHER CASE"""
        if len(ean13_code) !=13:
            raise OrderManagementException("Invalid ean13 code: not a 13 digit string")
        if str(EAN13(ean13_code).calculate_checksum()) != ean13_code[-1]:
            raise OrderManagementException("Invalid ean13 code: check digit is incorrect")


    def validate_order_type(cls, order_type): #TODO ask about case sensitivity
        """RETURNS ORDER TYPE IF VALID OR THROWS AN EXCEPTION"""
        if not isinstance(order_type, str):
            raise OrderManagementException("Invalid order type: not a string")
        order_type.lower()
        if order_type in ["regular", "premium"]:
            return order_type
        raise OrderManagementException("Invalid order type: string is invalid")

    @classmethod
    def validate_address(cls, address): #TODO does between mean including 20 and 100 or not including
        if not isinstance(address, str):
            raise OrderManagementException("Invalid address: address is not a string")
        if len(address) > 100:
            raise OrderManagementException("Invalid address: address is too long")
        if len(address) < 20:
            raise OrderManagementException("Invalid address: address is too short")
        if " " not in address:
            raise OrderManagementException("Invalid address: address should contain a space")
        return address

    @classmethod
    def validate_phone_number(cls, phone_number): # TODO is the prefix 211 or 34
        if not isinstance(phone_number, str):
            raise OrderManagementException("Invalid phone number: phone number is not a string")
        if len(phone_number) > 12:
            raise OrderManagementException("Invalid phone number: phone number is too long")
        if len(phone_number) < 12:
            raise OrderManagementException("Invalid phone number: phone number is too short")
        if phone_number[0 : 2] != "+34":
            raise OrderManagementException("Invalid phone number: wrong area code")
        return phone_number

    @classmethod
    def validate_zip_code(cls, zip_code: str): #TODO is the range correct
        if not isinstance(zip_code, str):
            raise OrderManagementException("Invalid zip code: zip code not a string")
        if not len(zip_code) == 5:
            raise OrderManagementException("Invalid zip code: zip code not 5 characters")
        if not zip_code.isdigit():
            raise OrderManagementException("Invalid zip code: characters are not digits")
        if int(zip_code) < 1001:
            return OrderManagementException("Invalid zip code: zip code is below range")
        if int(zip_code) > 52006:
            return OrderManagementException("Invalid zip code: zip code is above range")
        return zip_code

    # pylint: disable=too-many-arguments
    def register_order(self, product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: str) -> str:

        # check validity all of the arguments
        self.validate_ean13(product_id)
        self.validate_order_type(order_type)
        self.validate_address(address)
        self.validate_phone_number(phone_number)
        self.validate_zip_code(zip_code)

        order_request = OrderRequest(product_id, order_type, address, phone_number,zip_code)

        try:
            with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
                data = json.load(file)
            data.append(order_request.to_json())
            file.seek(0)
            json.dump(data, file, indent=4)
        except FileNotFoundError as exception: # TODO is this the more specific exception
            raise OrderManagementException("Could not write to file") from exception
        return order_request.order_id


    # def send_product (self,input_file_path: str): # SECOND function
    #     with ()
    #         dict1 = json.load(input_file_path) # TODO not named dict
    #
    #     if "OrderId" not in dict1:
    #         print("fixme")
    #         # TODO throw exception
    #     a = dict1['order_id']
    #     self.validate_orderId(a) # TODO this method doesn't exist... do we make it?
    #
    #
    #
            #TODO
        # validate input file path by checkign that the file exists and that we can read from it
        # (use self asserts?)
        # check file exists
        # check that the file is a json
        # extract data from json (OrderRequest object)
        # check that the order id is valid
        # create the OrderShipping object
        # write to order shipping object to file
        # return the SHA256 of the Ordershipping object
