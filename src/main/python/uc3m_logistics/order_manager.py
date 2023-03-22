"""Module """
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
        print("Order request store: ", self.__order_request_json_store)
        try:
            if not os.path...

        # TODO: assign path variables
        # and ensure that the files exist

    @staticmethod
    def validate_ean13(cls, ean13_code):
        """RETURNS TRUE IF THE CODE RECEIVED IS A VALID EAN13,
        OR FALSE IN OTHER CASE"""
        if len(ean13_code) !=13:
            raise OrderManagementException("Invalid ean13 code: not a 13 digit string")
        if str(EAN13(ean13_code).calculate_checksum()) != ean13_code[-1]:
            raise OrderManagementException("Invalid ean13 code: check digit is incorrect")


    def validate_order_type(cls, order_type):

        if not isinstance(order_type, str):
            raise OrderManagementException("Invalid order type: not a string")
        if order_type not in ["Regular", "Premium"]:
            return order_type ## TODO double check

    @classmethod
    def validate_address(cls, address):
        if not isinstance(address, str):
            raise OrderManagementException("Address is not a string")
        return address

    @classmethod
    def validate_phone_number(cls, phone_number):
        # TODO: deal with prefix and also check phone number in general
        # TODO i.e. all digits and doesn't start with 211
        return phone_number

    @classmethod
    def validate_zip_code(cls, zip_code:str):
        if not isinstance(zip_code, str):
            raise OrderManagementException("Invalid zip code: not a string")
        if not len(zip_code) == 5:
            raise OrderManagementException("Invalid zip code: zip code not 5 characters")
        if not zip_code.isdigit():
            raise OrderManagementException("Invalid zip code: characters are not digits")
        if not (1 <= int(zip_code[:2]) <= 52):
            # TODO: is this right
            return OrderManagementException("Invalid zip code: prefix invalid")
        return zip_code

    # pylint: disable=too-many-arguments
    def register_order(self, product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: int) -> str:

        # check validity all of the arguments
        self.validate_ean13(product_id)
        self.validate_order_type(order_type)
        self.validate_address(address)
        self.validate_phone_number(phone_number)
        self.validate_zip_code(zip_code)

        order_request = OrderRequest(product_id, order_type, address, phone_number,zip_code)

        # TODO: turn this into a try-catch block
        try:
            with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            data = json.load(file)
            data.append(order_request.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
        catch:

        return order_request.order_id


    def send_product (self,input_file_path: str):
        with ()
            dict1 = json.load(input_file_path) # TODO not named dict

        if "OrderId" not in dict1:
            print("fixme")
            # TODO throw exception
        a = dict1['order_id']
        self.validate_orderId(a) # TODO this method doesn't exist... do we make it?




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
