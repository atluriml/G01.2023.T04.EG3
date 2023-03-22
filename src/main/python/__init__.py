def to_json(self):
    return {
        "tracking_id": #todo here
        "order_id": self.order_id,
        "product_id": self.__product_id,
        "delivery_address": self.__delivery_address,
        "order_type": self.__order_type,
        "phone_number": self.__phone_number,
        "zip_code": self.__zip_code,
        "time_stamp": self.__time_stamp,
    }