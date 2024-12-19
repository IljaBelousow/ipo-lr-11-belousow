import json
from transport.vehicle import Vehicle
from transport.van import Van
from transport.airplane import Airplane
from transport.client import Client

class TransportCompany:
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Название компании должно быть нормальным.")
        
        self.name = name
        self.vehicles = []
        self.clients = []

    def save_transports(self):
        transports_data = []
        for vehicle in self.vehicles:
            vehicle_data = vehicle.__dict__.copy() 
            vehicle_data['client_list'] = [client.name for client in vehicle.client_list]
            transports_data.append(vehicle_data)
        with open("transports.json", 'w', encoding='utf-8') as file:
            json.dump(transports_data, file, ensure_ascii=False, indent=4)

    def save_clients(self):
        clients_data = [client.__dict__ for client in self.clients]
        with open("clients.json", 'w', encoding='utf-8') as file:
            json.dump(clients_data, file, ensure_ascii=False, indent=4)


    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Это не транспортное средство.")
        
        self.vehicles.append(vehicle)
        self.save_transports()

    def list_vehicles(self):
        return f"Транспорт:\n" + "\n".join([f"  - {vehicle}" for vehicle in self.vehicles])
    
    def show_all_results(self):
        print("Транспорт:")
        
        airplanes = [vehicle for vehicle in self.vehicles if isinstance(vehicle, Airplane)]
        vans = [vehicle for vehicle in self.vehicles if isinstance(vehicle, Van)]

        if airplanes:
            print("Самолеты:")
            for airplane in airplanes:
                print(f"  - {airplane}")
        else:
            print("Нет доступных самолетов.")

        if vans:
            print("Фургоны:")
            for van in vans:
                print(f"  - {van}")
        else:
            print("Нет доступных фургонов.")

        print("Клиенты:")
        for client in self.clients:
            print(f"  - {client.name}, Груз: {client.cargo_weight}т, VIP: {'Да' if client.is_vip else 'Нет'}")

    def add_client(self, client):
        if not isinstance(client, Client):
            raise ValueError("Это не клиент помоему, введите нормально")
        
        self.clients.append(client)
        self.save_clients()

    def del_client(self, client_name):
        self.clients = [client for client in self.clients if client.name != client_name]
        self.save_clients()

    def del_vehicle(self, vehicle_id):
        self.vehicles = [vehicle for vehicle in self.vehicles if vehicle.vehicle_id != vehicle_id]
        self.save_transports()

    @staticmethod
    def sort_key(client):
        return (not client.is_vip)
    
    def optimize_cargo_distribution(self):
        sort_client = sorted(self.clients, key=self.sort_key)

        for client in sort_client:
            for vehicle in self.vehicles:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.load_cargo(client)  # Загружаем клиента
                    print(f"  В транспорт {vehicle.vehicle_id} загружено {client.cargo_weight}т клиентом {client.name}.")
                    self.del_client(client.name)  # Удаляем клиента из списка
                    break
                else:
                    print(f"  Нет транспорта для груза {client.cargo_weight}т клиента {client.name}.")

                

