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

    # Область для вывода значений
    output_area = ft.Text("", size=20, color="#fafafa")

    # Список для отображения добавленных клиентов
    added_clients_list = ft.Container(
        content=ft.ListView(
            auto_scroll=True,
            height=150,  # Устанавливаем высоту, чтобы отображать 5 строк
            spacing=5,
        ),
        bgcolor=ft.colors.BLACK,  # Цвет фона контейнера
    )

    # При KeyError
    error_dialog = ft.AlertDialog(
        title=ft.Text("404 KeyError 404"),
        content=ft.Text("Ошибка. Введите значение из Меню"),
    )

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
            output_area.value = "Клиент добавлен"
            
            # Добавляем информацию о клиенте в список
            added_clients_list.content.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(name, color="#fafafa"),  # Цвет текста
                        ft.Text(str(cargo_weight), color="#fafafa"),  # Цвет текста
                        ft.Text("Да" if is_vip else "Нет", color="#fafafa"),  # Цвет текста
                    ]),
                    padding=10,
                    bgcolor=ft.colors.PURPLE_900,  # Цвет фона контейнера
                    border_radius=5,
                )
            )
            page.update()
        except ValueError:
            output_area.value = "Введите нормальный вес груза"
        
        page.update()

    # Выводит значение
    def on_submit(e):
        if user_input.value == "7":
            output_area.value = "Закрыто"
            page.window_close()
            return
        else:
            try:
                output_area.value = f"Вы ввели: {menu_list[user_input.value]}"
                if user_input.value == "1":
                    add_client_dialog(e)
            except KeyError:
                output_area.value = "Поздравляю с ошибкой"
                page.open(error_dialog)
        
        user_input.value = ""
        page.update()

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
                added_clients_list,  # Список с клиентами
                input_row,  # Кнопки ввода и вывода, выравненные по центру
                ft.Row(     # Вывод значения
                    [
                        output_area,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([menu_item], alignment=ft.MainAxisAlignment.CENTER), # Меню
            ],
            alignment=ft.MainAxisAlignment.START,  # Выравнивание по началу
        )
    )
    
    menu()

ft.app(target=main, view=ft.AppView.FLET_APP)
