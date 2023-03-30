"""Order Manager File"""
import datetime
import json
import os
import string
from .order_shipping import OrderShipping
from .order_management_exception import OrderManagementException
from .order_id_not_found_exception import OrderidNotFoundException
from .order_request import OrderRequest

from freezegun import freeze_time
from datetime import datetime


class OrderManager:
    """Class for providing the methods for managing the orders"""

    def __init__(self):
        store_path = "../stores/"
        current_path = os.path.dirname(__file__)
        self.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")
        self.__order_manager_json_store = os.path.join(current_path, store_path, "order_manager.json")
        self.__order_shipping_json_store = os.path.join(current_path, store_path, "order_shipping.json")

        try:
            if not os.path.exists(self.__order_request_json_store):
                with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception:
            raise OrderManagementException("Could create/find order_request.json") from exception

        try:
            if not os.path.exists(self.__order_manager_json_store):
                with open(self.__order_manager_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception:
            raise OrderManagementException("Could create/find order_manager.json") from exception

        try:
            if not os.path.exists(self.__order_shipping_json_store):
                with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
                    file.write("[]")
        except FileNotFoundError as exception:
            raise OrderManagementException("Could create/find order_shipping.json") from exception

    @staticmethod
    def validate_ean13(ean13_code):
        """Returns ean13_code if valid, otherwise throws exception"""
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

    @classmethod
    def validate_order_type(cls, order_type):
        """Returns order_type if valid, otherwise throws exception"""
        if not isinstance(order_type, str):
            raise OrderManagementException("Invalid order type: not a string")
        order_type = order_type.lower()
        if order_type in ["regular", "premium"]:
            return order_type
        raise OrderManagementException("Invalid order type: string is invalid")

    @classmethod
    def validate_address(cls, address):
        """Returns address if valid, otherwise throws exception"""
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
    def validate_phone_number(cls, phone_number):
        """Returns phone_number if valid, otherwise throws exception"""
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
    def validate_zip_code(cls, zip_code: str):
        """Returns zipcode if valid, otherwise throws exception"""
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

    @classmethod
    def is_hexadecimal(self, check_string : str):
        for ch in check_string:
            if ch not in string.hexdigits:
                raise OrderManagementException("Given string is not hexadecimal")

    def validate_orderid(self, order_id):
        if not isinstance(order_id, str):
            raise OrderManagementException("Invalid OrderID: OrderID not a string")
        if len(order_id) != 32:
            raise OrderManagementException("Invalid OrderID: OrderID length not 32 characters")
        try:
            self.is_hexadecimal(order_id)
        except Exception as exception:
            raise OrderManagementException("Invalid OrderID: OrderID is not a hexadecimal") from exception

        # opening order request json
        with open(self.__order_request_json_store, "r+", encoding="utf-8") as file:
            data = json.load(file)
        if data["order_id"] == order_id:
            product_id = data["product_id"]
            order_type = data["order_type"]
            delivery_address = data["delivery_address"]
            delivery_phone_number = data["phone_number"]
            zip_code = data["zip_code"]
            expected_order_id = data["order_id"]
        else:
            raise OrderManagementException("Invalid OrderID: Order id is not in order request json")
        assert order_id == expected_order_id, "Invalid OrderID: order ids are not equal"
        return OrderRequest(product_id, order_type, delivery_address, delivery_phone_number, zip_code)

    @classmethod
    def validate_tracking_code(self, tracking_code):
        self.is_hexadecimal(tracking_code)

    # pylint: disable=too-many-arguments
    @freeze_time('2023-03-09')
    def register_order(self, product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: str) -> str:

        # check validity of the arguments
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
                json.dump(data, file, indent=4)
        except Exception as exception:
            raise OrderManagementException("Could not write to file order_request json") from exception
        return order_request.order_id

    @freeze_time('2023-03-09')
    def send_product(self, input_file_path: str):
        try:
            with open(input_file_path, "r+", encoding="utf-8") as file:
                data = json.load(file)
                if "OrderID" not in data:
                    raise OrderidNotFoundException("Send product: Input file does not have order id")
                order_id = data["OrderID"]
        except FileNotFoundError as exception:
            raise FileNotFoundError("Send product: Input file does not exist") from exception
        except json.decoder.JSONDecodeError as exception:
            raise json.decoder.JSONDecodeError("Send product: Input file json is incorrect", input_file_path, 0) from exception
        except OrderidNotFoundException as exception:
            raise OrderidNotFoundException(str(exception)) from exception
        except Exception as exception:
            raise OrderManagementException("Send product: Error with the input file") from exception

        order_request = self.validate_orderid(order_id)

        # creating order shipping object
        order_shipping = OrderShipping(order_request.product_id, order_request.order_id, order_request.phone_number, order_request.order_type)
        # opening order shipping json
        try:
            with open(self.__order_shipping_json_store, "r+", encoding="utf-8") as file:
                data = json.load(file)
                data.append(order_shipping.to_json())
                file.seek(0)
                json.dump(data, file, indent=4)
        except Exception as exception:
            raise OrderManagementException("Send product: Cannot write to Order Shipping file") from exception

        # tracking code of the shipping request is returned
        return order_shipping.tracking_code

    @freeze_time('2023-03-10')
    def deliver_product(self, tracking_code: str):
        self.validate_tracking_code(tracking_code)
        delivery_time = datetime.utcnow()
        delivery_day = datetime.timestamp(delivery_time)
        try:
            with open(self.__order_shipping_json_store, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as exception:
            raise OrderManagementException("Could not open order_shipping_json_store") from exception
        # loops through order_shipping json
        if data["tracking_code"] == tracking_code:
            if data["delivery_day"] != delivery_day:
                raise OrderManagementException("Deliver Product: Invalid delivery day")

            # creates json object for delivery
            delivery = {
                "tracking_code": tracking_code,
                "time_stamp": delivery_day
            }
            # opens order manager json which holds the delivery information
            try:
                with open(self.__order_manager_json_store, "r+", encoding="utf-8") as file:
                    data = json.load(file)
                    data.append(delivery)
                    file.seek(0)
                    json.dump(data, file, indent=4)
            except Exception as exception:
                raise OrderManagementException("Deliver Product: could not write tracking to file") from exception
            return True
        raise OrderManagementException("Deliver Product: Invalid tracking code")