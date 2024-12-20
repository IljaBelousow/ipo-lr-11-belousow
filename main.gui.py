import flet as ft
import json
from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.transportcompany import TransportCompany

def main(page: ft.Page):

    

    page.title = "Хз какая-то программа"
    page.theme_mode = "dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Устанавливаем размер окна
    page.window_width = 1000
    page.window_height = 800

# Список для отображения добавленных клиентов
    added_clients_list = ft.Container(
        content=ft.ListView(
            auto_scroll=True,
            height=150,  # Устанавливаем высоту, чтобы отображать 5 строк
            spacing=5,
        ),
        bgcolor=ft.colors.BLACK,  # Цвет фона контейнера
    )

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

    transports, clients = load_data()
    company = TransportCompany("Транспортная компания")

# Отображение клиентов из clients.json
    for client in clients:
        client_obj = Client(client['name'], client['cargo_weight'], client['is_vip'])
        company.add_client(client_obj)

        # Добавляем информацию о клиенте в список
        added_clients_list.content.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(client['name'], color="#fafafa"),  # Цвет текста
                    ft.Text(str(client['cargo_weight']), color="#fafafa"),  # Цвет текста
                    ft.Text("Да" if client['is_vip'] else "Нет", color="#fafafa"),  # Цвет текста
                ]),
                padding=10,
                border_radius=5,
            )
        )

# Отображение транспортных средств
    for transport in transports:
        if 'max_altitude' in transport:  
            vehicle = Airplane(transport['capacity'], transport['max_altitude'])
        else:  
            vehicle = Van(transport['capacity'], transport['is_refrigerated'])
        company.add_vehicle(vehicle)

    company.show_all_results()

    menu_item = ft.Text("")

    notModelWindow = ft.AlertDialog(
        title=ft.Text("Информация о программе"),
        content=ft.Column(
            controls=[
                ft.Text("ЛР 12 !!!"),
                ft.Text("Вариант 4"),
                ft.Text("Белоусов Илья Русланович"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            width=100,
            height=100,
        )
    )

    menu_list = {
        "1": "Добавить клиента", 
        "2": "Добавить транспорт", 
        "3": "Удалить клиента", 
        "4": "Удалить транспорт", 
        "5": "Распределить грузы", 
        "6": "Вывести все результаты", 
        "7": "Выйти из программы", 
    }

    # Модальное окно для отображения всех результатов в таблице
    def show_all_results_dialog():
        # Создаем таблицу для отображения результатов
        rows = []
        
        # Добавляем клиентов
        for client in company.clients:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(client.name)),
                    ft.DataCell(ft.Text(str(client.cargo_weight))),
                    ft.DataCell(ft.Text("Да" if client.is_vip else "Нет")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            )
        
        # Добавляем транспортные средства
        for vehicle in company.vehicles:
            load_status = f"{vehicle.current_load}/{vehicle.capacity}"  # Assuming vehicles have current_load attribute
            vehicle_type = vehicle.__class__.__name__  # Get the type of vehicle
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(vehicle_type)),  # Vehicle type
                    ft.DataCell(ft.Text(load_status)),  # Display load status
                ])
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Имя клиента")),
                ft.DataColumn(ft.Text("Вес груза")),
                ft.DataColumn(ft.Text("VIP")),
                ft.DataColumn(ft.Text("Тип транспорта")),
                ft.DataColumn(ft.Text("Загруженность")),
            ],
            rows=rows
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Все результаты"),
            content=table,
            actions=[
                ft.ElevatedButton("Закрыть", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

# Модальное окно для добавления транспортного средства
    def add_vehicle_dialog(e):
        vehicle_type_input = ft.Dropdown(
            label="Тип транспорта",
            options=[
                ft.dropdown.Option("Самолет"),
                ft.dropdown.Option("Фургон"),
            ],
            width=300
        )
        capacity_input = ft.TextField(label="Введите грузоподъемность", width=300)
        max_altitude_input = ft.TextField(label="Максимальная высота полёта", width=300, visible=False)
        is_refrigerated_input = ft.Checkbox(label="Холодильник", value=False)

        def on_vehicle_type_change(e):
            if vehicle_type_input.value == "Самолет":
                max_altitude_input.visible = True
                is_refrigerated_input.visible = False
            else:
                max_altitude_input.visible = False
                is_refrigerated_input.visible = True
            page.update()

        vehicle_type_input.on_change = on_vehicle_type_change

        dialog = ft.AlertDialog(
            title=ft.Text("Добавить транспортное средство"),
            content=ft.Column(
                controls=[
                    vehicle_type_input,
                    capacity_input,
                    max_altitude_input,
                    is_refrigerated_input,
                ],
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton("Добавить", on_click=lambda e: add_vehicle(vehicle_type_input.value, capacity_input.value, max_altitude_input.value, is_refrigerated_input.value)),
                ft.ElevatedButton("Отмена", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

    def add_vehicle(vehicle_type, capacity, max_altitude, is_refrigerated):
        try:
            capacity = float(capacity)
            if vehicle_type == "Самолет":
                max_altitude = float(max_altitude)
                vehicle = Airplane(capacity, max_altitude)
            else:
                vehicle = Van(capacity, is_refrigerated)  
                
            company.add_vehicle(vehicle)
            show_message_dialog("Транспортное средство добавлено.")
        except ValueError as e:
            show_error_dialog(str(e))  # Отображаем сообщение об ошибке


# Модальное окно для удаления транспортного средства
    def del_vehicle_dialog(e):
        vehicle_id_input = ft.TextField(label="Введите ID транспортного средства для удаления", width=300)
        dialog = ft.AlertDialog(
            title=ft.Text("Удалить транспортное средство"),
            content=ft.Column(
                controls=[
                    vehicle_id_input,
                ],
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton("Удалить", on_click=lambda e: del_vehicle(vehicle_id_input.value)),
                ft.ElevatedButton("Отмена", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

    def del_vehicle(vehicle_id):
        try:
            vehicle_id = int(vehicle_id)
            company.del_vehicle(vehicle_id)
            show_message_dialog(f"Транспортное средство с ID {vehicle_id} удалено.")
        except ValueError:
            show_error_dialog("Введите корректный ID транспортного средства.")

    def show_message_dialog(message):
        message_dialog = ft.AlertDialog(
            title=ft.Text("Сообщение"),
            content=ft.Text(message),
            actions=[
                ft.ElevatedButton("Закрыть", on_click=lambda e: page.close(message_dialog)),
            ],
        )
        page.open(message_dialog)


    def show_error_dialog(message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Ошибка"),
            content=ft.Text(message),
            actions=[
                ft.ElevatedButton("Закрыть", on_click=lambda e: page.close(error_dialog)),
            ],
        )
        page.open(error_dialog)

# Модальное окно для добавления клиента
    def add_client_dialog(e):
        name_input = ft.TextField(label="Введите имя клиента", width=300)
        cargo_weight_input = ft.TextField(label="Введите вес груза", width=300)
        is_vip_input = ft.Checkbox(label="VIP")

        dialog = ft.AlertDialog(
            title=ft.Text("Добавить клиента"),
            content=ft.Column(
                controls=[
                    name_input,
                    cargo_weight_input,
                    is_vip_input,
                ],
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton("Добавить", on_click=lambda e: add_client(name_input.value, cargo_weight_input.value, is_vip_input.value)),
                ft.ElevatedButton("Отмена", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

    def add_client(name, cargo_weight, is_vip):
        try:
            cargo_weight = float(cargo_weight)
            client = Client(name, cargo_weight, is_vip)
            company.add_client(client)
            show_message_dialog("Клиент добавлен")
            
            # Добавляем информацию о клиенте в список
            added_clients_list.content.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(name, color="#fafafa"),  # Цвет текста
                        ft.Text(str(cargo_weight), color="#fafafa"),  # Цвет текста
                        ft.Text("Да" if is_vip else "Нет", color="#fafafa"),  # Цвет текста
                    ]),
                    padding=10,
                    border_radius=5,
                )
            )
            page.update()
        except ValueError:
            show_error_dialog("Введите нормально")  # Вызов функции для отображения ошибки

# Модальное окно для удаления клиента
    def del_client_dialog(e):
        name_input = ft.TextField(label="Введите имя клиента для удаления", width=300)
        dialog = ft.AlertDialog(
            title=ft.Text("Удалить клиента"),
            content=ft.Column(
                controls=[
                    name_input,
                ],
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton("Удалить", on_click=lambda e: del_client(name_input.value)),
                ft.ElevatedButton("Отмена", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

    def del_client(name):
        if company.del_client(name):  # Удаляем клиента из компании
            show_message_dialog(f"Клиент '{name}' удален")
            
            # Обновляем список клиентов в added_clients_list
            added_clients_list.content.controls = [
                ft.Container(
                    content=ft.Row([
                        ft.Text(client.name, color="#fafafa"),
                        ft.Text(str(client.cargo_weight), color="#fafafa"),
                        ft.Text("Да" if client.is_vip else "Нет", color="#fafafa"),
                    ]),
                    padding=10,
                    border_radius=5,
                ) for client in company.clients  # Перебираем клиентов в компании
            ]
            page.update()  # Обновляем страницу после изменения списка клиентов
        else:
            show_error_dialog(f"Клиент '{name}' не найден")
            page.update()  # Обновляем страницу для отображения сообщения об ошибке

# Выводит значение
    def on_submit(e):
        try:
            choice = int(user_input.value)  # Ввод в целое число
            if choice == 1:
                add_client_dialog(e)  # Для добавления клиента
            elif choice == 2:
                add_vehicle_dialog(e)  # Для добавления транспортного средства
            elif choice == 3:
                del_client_dialog(e)  # Для удаления клиента
            elif choice == 4:
                del_vehicle_dialog(e)  # Для удаления транспортного средства
            elif choice == 5:
                company.optimize_cargo_distribution()  # Распределяем грузы
                show_message_dialog("Грузы распределены.")
            elif choice == 6:
                show_all_results_dialog()  # Отображаем все результаты в диалоговом окне
            elif choice == 7:
                show_message_dialog("Закрыто")
                page.window_close()
                return
            else:
                show_error_dialog("Введите число от 1 до 7")  # Ошибка для некорректного ввода
        except ValueError:
            show_error_dialog("Введите корректное число")  # Ошибка для некорректного ввода
        except KeyError:
            show_error_dialog("Ошибка. Введите значение из меню")  # Ошибка для некорректного ввода
        finally:
            user_input.value = ""  # Очищаем поле ввода
            page.update()  # Обновляем страницу

# Создание поля для ввода действия
    user_input = ft.TextField(
        label="Введите действие", 
        width=300, 
        multiline=True
    )

# Кнопка для отправки
    submit_button = ft.ElevatedButton(text="Отправить", on_click=on_submit)

# Выравнение по центру
    input_row = ft.Row(
        [
            user_input, 
            submit_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def menu():
        menu_text = "\n".join([f"{key} - {value}" for key, value in menu_list.items()])
        menu_item.value = "Меню:\n" + menu_text
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.add(
        ft.Column(  # Column для вертикального расположения элементов
            controls=[
                ft.Row(     # Сменить цвет
                    [
                        ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                        ft.Text("Сменить цвет интерфейса", color="#fafafa")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(     # Диалоговое О программе
                    [
                        ft.IconButton(ft.icons.EXPLICIT_SHARP, on_click=lambda e: page.open(notModelWindow)),
                        ft.Text("О программе", color="#fafafa")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                # Список с клиентами
                input_row,  # Кнопки ввода и вывода, выравненные по центру
                ft.Row([menu_item], alignment=ft.MainAxisAlignment.CENTER), # Меню
            ],
            alignment=ft.MainAxisAlignment.START,  # Выравнивание по началу
        )
    )

    menu()
ft.app(target=main, view=ft.AppView.FLET_APP)