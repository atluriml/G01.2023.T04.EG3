"""Module"""
import json
import os
import string

from barcode import EAN13

from .order_shipping import OrderShipping
from .order_management_exception import OrderManagementException
from .order_id_not_found_exception import OrderidNotFoundException
from .order_request import OrderRequest

from freezegun import freeze_time


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
        except FileNotFoundError as exception:  # finish
            raise OrderManagementException("Could create/find order_request.json") from exception

        try:
            if not os.path.exists(self.__order_manager_json_store):
                with open(self.__order_manager_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception:  # finish
            raise OrderManagementException("Could create/find order_manager.json") from exception

        try:
            if not os.path.exists(self.__order_shipping_json_store):
                with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception:  # finish
            raise OrderManagementException("Could create/find order_shipping.json") from exception

    @staticmethod
    def validate_ean13(ean13_code):
        """RETURNS TRUE IF THE CODE RECEIVED IS A VALID EAN13,
        OR FALSE IN OTHER CASE"""
        if len(ean13_code) != 13:
            raise OrderManagementException("Invalid ean13 code: not a 13 digit string")
        if not ean13_code.isdigit():
            raise OrderManagementException("Invalid ean13 code: not a 13 digit string")
        barcode_sum = 0
        for i in range(0, len(ean13_code), 1):
            if i == len(ean13_code) - 1:
                continue
            if i % 2 == 0:  # if the position is even, the weight is 3
                barcode_sum += (1 * int(ean13_code[i]))
            else:
                barcode_sum += (3 * int(ean13_code[i]))
        # validate checkdigit
        if barcode_sum % 10 == 0:
            expected_checkdigit = (int(barcode_sum / 10) * 10) - barcode_sum
        else:
            expected_checkdigit = \
                ((int(barcode_sum / 10) + 1) * 10) - barcode_sum
        if not expected_checkdigit == int(ean13_code[-1]):
            raise OrderManagementException("Invalid ean13 code: check digit is incorrect")
        return ean13_code

    def validate_order_type(cls, order_type):
        """RETURNS ORDER TYPE IF VALID OR THROWS AN EXCEPTION"""
        if not isinstance(order_type, str):
            raise OrderManagementException("Invalid order type: not a string")
        order_type = order_type.lower()
        if order_type in ["regular", "premium"]:
            return order_type
        raise OrderManagementException("Invalid order type: string is invalid")

    @classmethod
    def validate_address(cls,
                         address):  # TODO does between mean including 20 and 100 or not including include in write-up
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
    def validate_phone_number(cls, phone_number):  # TODO is the prefix 211 or 34
        if not isinstance(phone_number, str):
            raise OrderManagementException("Invalid phone number: phone number is not a string")
        if len(phone_number) > 12:
            raise OrderManagementException("Invalid phone number: phone number is too long")
        if len(phone_number) < 12:
            raise OrderManagementException("Invalid phone number: phone number is too short")
        if phone_number[0:3] != "+34":
            raise OrderManagementException("Invalid phone number: wrong area code")
        return phone_number

    @classmethod
    def validate_zip_code(cls, zip_code: str):  # TODO is the range correct
        if not isinstance(zip_code, str):
            raise OrderManagementException("Invalid zip code: zip code not a string")
        if not len(zip_code) == 5:
            raise OrderManagementException("Invalid zip code: zip code not 5 characters")
        if not zip_code.isdigit():
            raise OrderManagementException("Invalid zip code: characters are not digits")
        if int(zip_code) < 1001:
            raise OrderManagementException("Invalid zip code: zip code is below range")
        if int(zip_code) > 52006:
            raise OrderManagementException("Invalid zip code: zip code is above range")
        return zip_code

    # pylint: disable=too-many-arguments
    @freeze_time('2023-03-09')
    def register_order(self, product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: str) -> str:

        # check validity all of the arguments
        self.validate_ean13(product_id)
        self.validate_order_type(order_type)
        self.validate_address(address)
        self.validate_phone_number(phone_number)
        self.validate_zip_code(zip_code)

        order_request = OrderRequest(product_id, order_type, address, phone_number, zip_code)

        try:
            with open(self.__order_request_json_store, "r+", encoding="utf-8") as file:
                data = json.load(file)
                data.append(order_request.to_json())
                file.seek(0)
                print(data)
                json.dump(data, file, indent=4)
        except Exception as exception:
            raise OrderManagementException("Could not write to file") from exception
        return order_request.order_id

    def is_hexadecimal(self, string):
        if not isinstance(string, str):
            raise OrderManagementException("Invalid OrderID: OrderID not a string")
        if len(string) != 32:
            raise OrderManagementException("Invalid OrderID: OrderID length not 32 characters")
        for ch in string:
            if ch not in string.hexdigits:
                raise OrderManagementException("Invalid OrderID: orderID not hexadecimal")

    def validate_orderid(self, order_id):
        try:
            self.is_hexadecimal(order_id)
        except Exception as exception:
            raise OrderManagementException(str(exception))

        with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "order_id" not in data:
                raise OrderidNotFoundException("order id is not found")
            expected_order_id = data["order_id"]
        if not self.assertEqual(order_id, expected_order_id):
            raise Exception("order id is not valid")

    def send_product(self, input_file_path: str):  # SECOND function
        try:
            with open(input_file_path, "r+", encoding="utf-8") as file:
                data = json.load(file)
                if "OrderID" not in data:
                    raise OrderidNotFoundException("order id not found")
                order_id = data["OrderID"]
                self.validate_orderid(order_id)
        except FileNotFoundError as exception:
            raise FileNotFoundError(str(exception))
        except json.decoder.JSONDecodeError as exception:
            raise json.decoder.JSONDecodeError(str(exception), input_file_path, 0)
        except OrderidNotFoundException as exception:
            raise OrderidNotFoundException(str(exception))
        except Exception as exception:
            raise OrderManagementException(str(exception))

        #
        #     if "OrderId" not in dict1:
        #         print("fixme")
        #         # TODO throw exception
        #

        shipping = OrderShipping(data.product_id, data.order_id, data.delivery_phone_number, data.order_type)

        json.dump(shipping, self.__order_shipping_json_store, indent=4)

        return shipping.alg()

        # TODO
        # validate input file path by checkign that the file exists and that we can read from it
        # (use self asserts?)
        # check file exists
        # check that the file is a json
        # extract data from json (OrderRequest object)
        # check that the order id is valid
        # create the OrderShipping object
        # write to order shipping object to file
        # return the SHA256 of the Ordershipping object

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
