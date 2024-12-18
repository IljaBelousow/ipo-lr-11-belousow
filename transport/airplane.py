from transport.vehicle import Vehicle
from transport.van import Van
from transport.airplane import Airplane
from transport.client import Client
from main import save_transports
from main import save_clients

class Airplane(Vehicle):
    def __init__(self, capacity, max_altitude):
        super().__init__(capacity)
        if not isinstance(max_altitude, (int, float)) or max_altitude <= 0:
            raise ValueError("Максимальная высота полета должна быть ХОТЯ БЫ больше 0")
        
        self.max_altitude = max_altitude