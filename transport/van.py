from transport.vehicle import Vehicle
from transport.van import Van
from transport.airplane import Airplane
from transport.client import Client
from main import save_transports
from main import save_clients

class Van(Vehicle):
    def __init__(self, capacity, is_refrigerated):
        super().__init__(capacity)
        self.is_refrigerated = is_refrigerated.lower() == "да"
