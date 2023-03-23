"""class for testing the regsiter_order method"""
import os
import unittest
from uc3m_logistics import OrderManager, OrderRequest, OrderManagementException

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    @classmethod
    def setUpClass(cls) -> None:
        store_path = "../../main/python/stores/"
        current_path = os.path.dirname(__file__)
        cls.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")

    def set_up(self):
        with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def tear_down(self) -> None:
        #TODO
        return 0

    # todo: figure out @freeze_time
    def test_something( self ):
        """dummy test"""
        # TODO

        #with open(self.__order_request_json_s)

        # order_id_check = OrderRequest(product_id, order_type, delivery_address, ...)

        self.assertEqual(True, False)

    # def validate_order_id(self):


    # TODO check if this is the correct format
    # product id tests
    def test_product_id_valid(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_product_id_not_number(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("842169142322A", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")
    def test_product_id_invalid_checksum(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8421691423222", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: check digit is incorrect")
    def test_product_id_invalid_too_short(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")
    def test_product_id_invalid_too_long(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+13", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid ean13 code: not a 13 digit string")

    # order type tests
    def test_order_type_valid_regular(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))

    def test_order_type_valid_premium(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Premium", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Premium", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))

    def test_order_type_invalid_wrong(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "PRE", "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid order type: string is invalid")

    def test_order_type_not_string(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", 333, "C/LISBOA,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid order type: not a string")

    # address tests
    def test_address_valid(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))

    def test_address_not_string(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", 333, "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is not a string")

    def test_address_invalid_too_long(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "CALLE DE VALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSOVALLHERMOSO,4, MADRID, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is too long")

    def test_address_invalid_too_short(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/ ALLE, SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address is too short")

    def test_address_invalid_no_space(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4,MADRID,SPAIN", "+34123456789",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid address: address should contain a space")

    # phone number tests
    def test_phone_number_valid(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))

    def test_phone_number_not_string(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN", 34123456789,
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is not a string")

    def test_phone_number_too_long(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+341234567899",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is too long")

    def test_phone_number_too_short(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+3412345678",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: phone number is too short")

    def test_phone_number_invalid_area_code(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+441234567899",
                                                "28005")
        self.assertEqual(exception.exception.message, "Invalid phone number: wrong area code")

    # zipcode tests
    def test_zip_code_valid(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
        self.assertIsNotNone(
            self.__order_manager.register_order("8.42169E+12", "Regular", "C/LISBOA,4, MADRID, SPAIN", "+34123456789", "28005"))
    def test_zip_code_not_string(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                28005)
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code not a string")
    def test_zip_code_invalid_length(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "280005")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code not 5 characters")
    def test_zip_code_not_digits(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "28A05")
        self.assertEqual(exception.exception.message, "Invalid zip code: characters are not digits")
    def test_zip_code_under_range(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "01001")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code is below range")
    def test_zip_code_above_range(self):
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.register_order("8.42169E+11", "Regular", "C/LISBOA,4, MADRID, SPAIN",  "+34123456789",
                                                "52006")
        self.assertEqual(exception.exception.message, "Invalid zip code: zip code is above range")



if __name__ == '__main__':
    unittest.main()
