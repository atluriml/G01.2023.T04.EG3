"""Exception for the order_management module"""

class OrderidNotFoundException(Exception):
    """Personalised exception for Order ID not being found"""
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """gets the message value"""
        return self.__message

    @message.setter
    def message(self,value):
        self.__message = value
