#TODO
 # write a for loop: watch for the exceptions
import json
import os
import unittest

from uc3m_logistics import OrderManager, OrderRequest, OrderManagementException
from uc3m_logistics.order_id_not_found_exception import OrderidNotFoundException


class SendProductTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        store_path = "../../main/python/stores/"
        current_path = os.path.dirname(__file__)
        cls.__order_shipping_json_store = os.path.join(current_path, store_path, "order_shipping.json")
        cls.__order_request_json_store = os.path.join(current_path, store_path, "order_request.json")
        cls.__order_manager = OrderManager()

        # order_id = '7628fa19bcb8e965bb73f8a180718f99'
        product_id = "8421691423220"
        delivery_address = "C/LISBOA,4, MADRID, SPAIN"
        order_type = "Regular"
        phone_number = "+34123456789"
        zip_code = "28005"
        time_stamp =  "1678320000.0"

        order_request = OrderRequest(product_id, order_type, delivery_address, phone_number, zip_code)

        with open(cls.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write(str(order_request.to_json()))

    def setUp(self):
        with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def tearDown(self):
        with open(self.__order_shipping_json_store, "w", encoding="utf-8") as file:
            file.write("[]")
        with open(self.__order_request_json_store, "w", encoding="utf-8") as file:
            file.write("[]")

    def single_file_test(self, file_path):
        try:
            self.__order_manager.send_product(file_path)
            print(file_path, " : ", "No error!")
        except FileNotFoundError as exception:
            raise FileNotFoundError(str(exception))
        except json.decoder.JSONDecodeError as exception:
            raise json.decoder.JSONDecodeError(str(exception), file_path, 0)
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
                if filename[0] == '.': # If the file is hidden
                    continue
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except json.decoder.JSONDecodeError as exception:
                print("expected exception: ", str(exception))
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))

        directory = 'send_product_tests/order_id_not_found_error'
        for filename in os.listdir(directory):
            try:
                if filename[0] == '.': # If the file is hidden
                    continue
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except OrderidNotFoundException as exception:
                print("expected exception: ", str(exception))
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))

        directory = 'send_product_tests/order_management_error'
        for filename in os.listdir(directory):
            try:
                if filename[0] == '.': # If the file is hidden
                    continue
                file_path = os.path.join(directory, filename)
                self.single_file_test(file_path)
            except OrderManagementException as exception:
                print("expected exception: ", str(exception))
            except Exception as exception:
                print("Non-expected exception")
                raise Exception(str(exception))


