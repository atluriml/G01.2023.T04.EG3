import json
import os
import unittest

from uc3m_logistics import OrderManager, OrderRequest, OrderManagementException, OrderShipping
from uc3m_logistics.order_id_not_found_exception import OrderidNotFoundException

class DeliverProductTests(unittest.TestCase):

    __order_shipping_json_store = None

    @classmethod
    def setUpClass(cls) -> None:
        store_path = "../../main/python/stores/"
        current_path = os.path.dirname(__file__)
        cls.__order_shipping_json_store = os.path.join(current_path, store_path, "order_shipping.json")
        cls.__order_manager_json_store = os.path.join(current_path, store_path, "order_manager.json")
        cls.__order_manager = OrderManager()

        product_id = "8421691423220"
        order_id = "7628fa19bcb8e965bb73f8a180718f99"
        phone_number = "+34123456789"
        order_type = "Premium"

        order_shipping = OrderShipping(product_id, order_id, phone_number, order_type)
        with open(cls.__order_shipping_json_store, "w+", encoding="utf-8") as file:
            order_shipping_json = order_shipping.to_json()
            json.dump(order_shipping_json, file, indent=4)

    def setUp(self):
        with open(self.__order_manager_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def tearDown(self):
        with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
            file.write("[]")
        with open(self.__order_manager_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def obtain_generated_tracking_code(self):
        with open(self.__order_shipping_json_store, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "tracking_code" not in data:
                raise OrderidNotFoundException("File does not have tracking code")
            tracking_code = data["tracking_code"]
        return tracking_code

    def test_path_1(self):
        tracking_code = self.obtain_generated_tracking_code()
        self.assertTrue(self.__order_manager.deliver_product(tracking_code))

    def test_path_2(self):
        # should throw an OME because it is not a hexadecimal
        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.deliver_product("tracking_code")
        self.assertEqual(exception.exception.message, "Given string is not hexadecimal")

    def test_path_3(self):
        #todo not sure how to test to when order shipping json fails to open
        return False
    def test_path_4(self):
        # should raise OME exception due to delivery date being wrong
        product_id = "8421691423220"
        order_id = "7628fa19bcb8e965bb73f8a180718f99"
        phone_number = "+34123456789"
        order_type = "Regular"

        order_shipping = OrderShipping(product_id, order_id, phone_number, order_type)
        with open(self.__order_shipping_json_store, "w+", encoding="utf-8") as file:
            order_shipping_json = order_shipping.to_json()
            json.dump(order_shipping_json, file, indent=4)

        with self.assertRaises(OrderManagementException) as exception:
            self.__order_manager.deliver_product(self.obtain_generated_tracking_code())
        self.assertEqual(exception.exception.message, "Deliver Product: Invalid delivery day")

    def test_path_5(self):
        # todo should raise OME exception when trying to write to order manager json file
        return False

    def test_path_6(self):
        # when handling multiple entries
        product_id = "8421691423220"
        order_id = "7628fa19bcb8e965bb73f8a180718f99"
        phone_number = "+34123456789"
        order_type = "Premium"

        order_shipping = OrderShipping(product_id, order_id, phone_number, order_type)
        with open(self.__order_shipping_json_store, "w+", encoding="utf-8") as file:
            order_shipping_json = order_shipping.to_json()
            json.dump(order_shipping_json, file, indent=4)

        tracking_code = self.obtain_generated_tracking_code()
        self.assertTrue(self.__order_manager.deliver_product(tracking_code))

if __name__ == '__main__':
    unittest.main()