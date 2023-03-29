"""class for testing the register_order method"""
import hashlib
import json
import os
import unittest
from datetime import datetime
from freezegun import freeze_time

from uc3m_logistics import OrderManager, OrderRequest, OrderManagementException

class RegisterOrderTests(unittest.TestCase):
    """class for testing the register_order method"""
    __order_request_json_store: str = None

    @classmethod
    def setUpClass(cls) -> None:
        """method sets up RegisterOrderTests class"""
        store_path = "../../main/python/stores/"
        current_path = os.path.dirname(__file__)
        cls.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")
        cls.__order_manager = OrderManager()


    def setUp(self):
        """method sets up order_request json"""
        with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def tearDown(self) -> None:
        """method tears down RegisterOrderTests class"""
        with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    # output tests
    @freeze_time("2023-03-09")
    def test_validate_output_content(self):
        """test id: CV_V_ 27"""
        product_id = '8421691423220'
        order_type = 'Regular'
        delivery_address = 'C/LISBOA,4, MADRID, SPAIN'
        phone_number = '+34123456789'
        zip_code = '28005'

        # opens the order request json
        with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            order_requests = json.load(file)
            previous_json_items = len(order_requests)

        # validates output content
        order_id = self.__order_manager.register_order(product_id, order_type, delivery_address, phone_number, zip_code)
        with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            order_requests = json.load(file)
            self.assertEqual(len(order_requests), previous_json_items + 1)
            order_request = order_requests[0]
            self.assertDictEqual(order_request, {
                'order_id': order_id,
                'product_id': product_id,
                'order_type': order_type,
                'delivery_address': delivery_address,
                'phone_number': phone_number,
                'zip_code': zip_code,
                'time_stamp': datetime.timestamp(datetime.utcnow()),
            })
    @freeze_time("2023-03-09")
    def test_validate_order_id(self):
        """test id: CV_V_28"""
        product_id = '8421691423220'
        order_type = 'Regular'
        delivery_address = 'C/LISBOA,4, MADRID, SPAIN'
        phone_number = '+34123456789'
        zip_code = '28005'

        order_id = self.__order_manager.register_order(product_id, order_type, delivery_address, phone_number, zip_code)

        # obtains order id from hash
        order_id_check = hashlib.md5(json.dumps({
            '_OrderRequest__product_id': product_id,
            '_OrderRequest__delivery_address': delivery_address,
            '_OrderRequest__order_type': order_type,
            '_OrderRequest__phone_number': phone_number,
            '_OrderRequest__zip_code': zip_code,
            '_OrderRequest__time_stamp': datetime.timestamp(datetime.utcnow()),
        }).encode(encoding="utf-8")).hexdigest()

        # checks if order id's are equal
        self.assertEqual(order_id, order_id_check)

    # product id tests
    def test_product_id_valid(self):
        """test id: CE_V_1, CE_V_7"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_product_id_not_number(self):
        """test id: CE_NV_2"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("842169142322A", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")
    def test_product_id_invalid_checksum(self):
        """test id: CE_NV_3"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423222", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: check digit is incorrect")
    def test_product_id_invalid_too_short(self):
        """test id: CE_NV_4"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("842169142322", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")
    def test_product_id_invalid_too_long(self):
        """test id: CE_NV_5"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("84216914232222", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")

    # order type tests
    def test_order_type_valid_regular(self):
        """test id: CE_V_8"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_order_type_valid_premium(self):
        """test id: CE_V_9"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Premium", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Premium", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_order_type_invalid_wrong(self):
        """test id: CE_NV_10"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "PRE", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid order type: string is invalid")
    def test_order_type_not_string(self):
        """test id: CE_NV_11"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", 333, "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid order type: not a string")

    # address tests
    def test_address_valid(self):
        """test id: CE_V_12"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_address_not_string(self):
        """test id: CE_NV_13"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", 333, "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is not a string")
    def test_address_invalid_too_long(self):
        """test id: CE_NV_14"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "CALLE DE VALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSO,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is too long")
    def test_address_invalid_too_short(self):
        """test id: CE_NV_15"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/ ALLE, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is too short")
    def test_address_invalid_no_space(self):
        """test id: CE_NV_16"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4,MADRID,SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address should contain a space")

    # phone number tests
    def test_phone_number_valid(self):
        """test id: CE_V_17"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_phone_number_not_string(self):
        """test id: CE_NV_18"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", 34123456789,
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is not a string")
    def test_phone_number_too_short(self):
        """test id: CE_NV_19"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+3412345678",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is too short")
    def test_phone_number_too_long(self):
        """test id: CE_NV_20"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+341234567899",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is too long")
    def test_phone_number_invalid_area_code(self):
        """test id: CE_NV_21"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+44123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: wrong area code")

    # zipcode tests
    def test_zip_code_valid(self):
        """test id: CE_V_21"""
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_zip_code_under_range(self):
        """test id: CE_NV_22"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "01000")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code is below range")
    def test_zip_code_above_range(self):
        """test id: CE_NV_23"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "52007")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code is above range")
    def test_zip_code_not_string(self):
        """test id: CE_NV_24"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                28005)
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code not a string")
    def test_zip_code_invalid_length(self):
        """test id: CE_NV_25"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "280005")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code not 5 characters")
    def test_zip_code_not_digits(self):
        """test id: CE_NV_26"""
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423220", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "28A05")
        self.assertEqual(exception.exception.message, "Invalid zip code: characters are not digits")

if __name__ == '__main__':
    unittest.main()
