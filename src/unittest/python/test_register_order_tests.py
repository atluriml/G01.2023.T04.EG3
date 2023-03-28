"""class for testing the regsiter_order method"""
import unittest
from uc3m_logistics import OrderManager, OrderRequest, OrderManagementException

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    def set_up(self):
        #TODO
        return 0

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

    def validate_order_id(self):


    def test_order_type_valid(self):
        self.assertIsNotNone(
            self.__order_manager.register_order("awdwad", "Regular", "Calle de la Luna 1", "666666666", "28B 001"))
        self.assertIsNotNone(
            self.__order_manager.register_order("awdwad", "Premium", "Calle de la Luna 1", "666666666", "28001"))

    def test_order_type_invalid(self):
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as error:
            self.__order_manager.register_order("8421691423224", "INVALID", "Calle de la Luna 1, P4 6*a", "666666666",
                                                "28001")
        self.assertEqual(error.exception.message, "Invalid order type: INVALID")


if __name__ == '__main__':
    unittest.main()
