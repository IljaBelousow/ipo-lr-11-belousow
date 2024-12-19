import random
from transport.client import Client

class Vehicle:
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом.")
        
        self.vehicle_id = self.generate_vehicle_id()
        self.capacity = capacity
        self.current_load = 0
        self.client_list = []

    @staticmethod
    def generate_vehicle_id():
        return random.randint(10000000, 99999999)

    def load_cargo(self, client):
        if not isinstance(client, Client):
            raise ValueError("Переданный объект не является клиентом.")
        
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Превышена грузоподъемность транспортного средства.")

        self.current_load += client.cargo_weight
        self.client_list.append(client)  
        print(f"Клиент {client.name} загружен в транспортное средство.")

    def __str__(self):
        return f"ID: {self.vehicle_id}, Грузопъёмность: {self.capacity}т, Текущая загрузка: {self.current_load}т"
