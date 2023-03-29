#TODO
 # write a for loop: watch for the exceptions
import json
import os
import unittest

from uc3m_logistics import OrderManager, OrderManagementException
from uc3m_logistics.order_id_not_found_exception import OrderidNotFoundException


class SendProductTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        store_path = "../../main/python/stores/"
        current_path = os.path.dirname(__file__)
        cls.__order_shipping_json_store = os.path.join(current_path, store_path, "order_shipping.json")
        cls.__order_manager = OrderManager()

    def setUp(self):
        with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def tearDown(self):
        with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def single_file_test(self, file_path):
        try:
            self.__order_manager.send_product(file_path)
            print(file_path, " : ", "No error!")
        except FileNotFoundError as exception:
            raise FileNotFoundError(str(exception))
        except json.decoder.JSONDecodeError as exception:
            raise json.decoder.JSONDecodeError(str(exception))
        except OrderidNotFoundException as exception:
            raise OrderidNotFoundException(str(exception))
        except OrderManagementException as exception:
            raise OrderManagementException(str(exception))
        except Exception as exception:
            raise Exception(str(exception))

    def test_everything(self):
        directory = 'send_product_tests/json_decode_error'
        for filename in os.listdir(directory):
            try:
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except json.decoder.JSONDecodeError as exception:
                print("expected exception")
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))

        directory = 'send_product_tests/order_id_not_found_error'
        for filename in os.listdir(directory):
            try:
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except OrderidNotFoundException as exception:
                print("expected exception")
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))

        directory = 'send_product_tests/order_management_error'
        for filename in os.listdir(directory):
            try:
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except OrderManagementException as exception:
                print("expected exception")
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))


