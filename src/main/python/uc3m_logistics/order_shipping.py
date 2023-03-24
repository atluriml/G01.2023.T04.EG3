"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib

class OrderShipping():
    """Class representing the information required for shipping of an order"""

    def __init__( self, product_id, order_id, delivery_phone_number, order_type ):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__product_id = product_id
        self.__order_id = order_id
        self.__delivery_phone_number = delivery_phone_number
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1

        #timestamp is represneted in seconds.microseconds
        #__delivery_day must be expressed in senconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)

    def to_json(self):
        return {
            "alg": self.__alg,
            "type": self.__type,
            "order_id": self.__order_id,
            "issued_at": self.__issued_at,
            "delivery_day": self.__delivery_day,
            "tracking_code": self.__tracking_code,
        }

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",order_id:" + \
           self.__order_id + ",issuedate:" + self.__issued_at + \
           ",deliveryday:" + self.__delivery_day + "}" #TODO do we need to need include the tracking code

    @property
    def alg( self ):
        return self.__alg
    @alg.setter
    def alg( self, value ):
        self.__alg= value

    @property
    def product_id( self ):
        """Property that represents the product_id of the patient"""
        return self.__product_id

    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def tracking_id( self ):
        """Property that represents the order_id"""
        return self.__order_id
    @tracking_id.setter
    def tracking_id( self, value ):
        self.__order_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the client"""
        return self.__delivery_phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__delivery_phone_number = value

    @property
    def tracking_code( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()
    #    return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def delivery_day( self ):
        """Returns the delivery day for the order"""
        return self.__delivery_day

    @delivery_day.setter
    def delivery_day(self, value):
        self.__delivery_day = value