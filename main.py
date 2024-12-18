import random
import json
from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.transportcompany import TransportCompany

def load_data():
    try:
        with open("transports.json", 'r', encoding='utf-8') as file:
            transports = json.load(file)
    except FileNotFoundError:
        transports = []

    try:
        with open("clients.json", 'r', encoding='utf-8') as file:
            clients = json.load(file)
    except FileNotFoundError:
        clients = []

    return transports, clients

def save_transports(transports):
    with open("transports.json", 'w', encoding='utf-8') as file:
        json.dump(transports, file, ensure_ascii=False, indent=4)

def save_clients(clients):
    with open("clients.json", 'w', encoding='utf-8') as file:
        json.dump(clients, file, ensure_ascii=False, indent=4)

def menu():
    print("""
        1 - Добавить клиента
        2 - Добавить транспорт
        3 - Удалить клиента
        4 - Удалить транспорт
        5 - Распределить грузы
        6 - Вывести все результаты
        7 - Выйти из программы
    """)

def end_see():
    print("Программа завершена.")
    return True 

def main():
    transports, clients = load_data()
    company = TransportCompany("Транспортная компания")
    
    for client in clients:
        client_obj = Client(client['name'], client['cargo_weight'], client['is_vip'])
        company.add_client(client_obj)

    for transport in transports:
        if 'max_altitude' in transport:  
            vehicle = Airplane(transport['capacity'], transport['max_altitude'])
        else:  
            vehicle = Van(transport['capacity'], transport['is_refrigerated'])
        company.add_vehicle(vehicle)

    company.show_all_results()

    save_clients([])

    brik_close = False 

    while not brik_close:
        menu()
        try:
            user_input = int(input("Введите действие какое хотите выполнить: "))
        except ValueError:
            print("Ошибка: Пожалуйста, введите число от 1 до 7")
            continue
        
        if user_input == 1:
            name = input("Введите имя клиента: ")
            try:
                cargo_weight = float(input("Введите вес груза: "))
            except ValueError:
                print("Введите нормальный вес груза")
                continue
            is_vip = input("VIP? (да/нет): ").lower() == "да"
            client = Client(name, cargo_weight, is_vip)
            company.add_client(client)
            print("Клиент добавлен")

        elif user_input == 2:
            try:
                capacity = float(input("Введите грузоподъемность: "))
            except ValueError:
                print("Введите нормальную грузоподъёмность")
                continue
            vehicle_type = input("Введите тип транспорта (самолет/фургон): ").lower()
            if vehicle_type == "самолет":
                max_altitude = float(input("Введите максимальную высоту полета: "))
                vehicle = Airplane(capacity, max_altitude)
            elif vehicle_type == "фургон":
                is_refrigerated = input("Холодильник? (да/нет): ")
                vehicle = Van(capacity, is_refrigerated)
            else:
                print("Некорректный тип транспорта")
                continue
            company.add_vehicle(vehicle)
            print("Транспорт добавлен")

        elif user_input == 3:
            client_name = input("Введите имя клиента для удаления: ")
            company.del_client(client_name)
            print("Клиент удален")
        elif user_input == 4:
            vehicle_id = int(input("Введите ID транспорта для удаления: "))
            company.del_vehicle(vehicle_id)
            print("Транспорт удален")

        elif user_input == 5:
            company.optimize_cargo_distribution()

        elif user_input == 6:
            company.show_all_results()

        elif user_input == 7:
            brik_close = end_see()

        else:
            print("EROR 404 ОШИБКА, Введите нормально пж")

if __name__ == "__main__":
    main()
