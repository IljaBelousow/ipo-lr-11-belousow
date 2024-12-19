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
        ),
        
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




    # Создание поля для ввода и вывода
    user_input = ft.TextField(
                label="Введите действие", 
                width=300, 
                multiline=True
    )

    # Область для вывода значений
    output_area = ft.Text("", size=20)

    # При KeyError
    error_dialog = ft.AlertDialog(
        title=ft.Text("404 KeyError 404"),
        content=ft.Text("Ошибка. Введите значение из Меню"),
    )

    # Выводит значение
    def on_submit(e):
        try:
            output_area.value = f"Вы ввели: {menu_list[user_input.value]}"
            user_input.value = ""
            page.update()
        except KeyError:
            output_area.value = f"Поздравляю с ошибкой"
            user_input.value = ""
            page.open(error_dialog)
            

    # Кнопка для отправки
    submit_button = ft.ElevatedButton(text="Отправить", on_click=on_submit)

    # Выравние по центру
    row = ft.Row(
        [
            user_input, submit_button,
        ],
        
    )




    def get_info(e):
        pass

    
    def menu():
        menu = """
            1 - Добавить клиента
            2 - Добавить транспорт
            3 - Удалить клиента
            4 - Удалить транспорт
            5 - Распределить грузы
            6 - Вывести все результаты
            7 - Выйти из программы
        """
        menu_item.value = "Меню:" + menu
        page.update()


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


    def end_see():
        print("Программа завершена.")
       

    def change_theme(e):
        page.theme_mode = "ligth" if page.theme_mode == "dark" else "dark"
        page.update()


    page.add(
        ft.Row(     #Сменить цвет
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Text("Сменить цвет интерфейса")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(     #Диалоговое О программе
            [
                ft.IconButton(ft.icons.EXPLICIT_SHARP, on_click=lambda e: page.open(notModelWindow)),
                ft.Text("О программе")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(     #Диалоговое KeyError
            [
                
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(     #Кнопки ввода и вывода
            [
                row,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(     #Вывод значения
            [
                output_area,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        
        
        ft.Row([menu_item], alignment=ft.MainAxisAlignment.CENTER), #Меню
        
    )
    
    menu()
    
    page.add(
        ft.Row(
            [

            ]
        )
    )
    

    

ft.app(target=main, view=ft.AppView.FLET_APP)


