"""class for testing the regsiter_order method"""
import json
import os
import unittest
import hashlib
from uc3m_logistics import OrderManager
from freezegun import freeze_time
import datetime

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    def setUpClass(cls) -> None:
        store_path = "../../main/python/stores"
        current_path = os.path.dirname(__file__)
        cls.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")

    def setUp(self):
        with open (self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")
        self.__order_manager = OrderManager()

    def tearDown(self) -> None:
        with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    @freeze_time("2023-03-09")
    def test_something( self ):
        """sample test"""
        order_id = self.__order_manager.register_order("1234567890123", "Regular", "Calle de la Luna 1", "66666666", "28001")
        with open(self.__order_request_json_store, "r", encoding="utf-8") as file:
            order_requests = json.load(file)
            self.assertEqual(len(order_requests), 1)
            self.assertEqual(True, False)
    ##TODO make sure you have the same state before and after you run the test

if __name__ == '__main__':
    unittest.main()
