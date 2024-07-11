import flet as ft
# from my_udp import *
from my_mqtt import publish_message
from json import dumps


def main(page: ft.Page):
    page.title = "红绿灯上位机控制"
    page.window_height = 300
    page.window_width = 300
    page.window_resizable = False
    page.window_maximizable = False

    def connect_to_mqtt_server():
        pass

    page.snack_bar = ft.SnackBar(ft.Text(""))

    def close_snack_bar():
        page.snack_bar.open = False

    def on_send_command_button_clicked(e):
        # send_to(
        #     "192.168.14.78",
        #     159,
        #     f"set {choose_index_line.value} {choose_color_line.value} 0;",
        # )
        payload = dumps({
            "color":choose_color_line.value,
            "index":choose_index_line.value
        })

        publish_message("traffic_light1/control",payload,qos=0)
        show_message("指令发送成功!")

    def show_message(message: str):
        snack_bar_text = message
        page.snack_bar.content = ft.Text(message)
        page.snack_bar.open = True
        page.update()

    choose_color_line = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="green", label="绿灯", fill_color=ft.colors.GREEN),
                ft.Radio(
                    value="red",
                    label="红灯",
                    fill_color=ft.colors.RED,
                ),
            ]
        )
    )

    choose_index_line = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="left", label="左"),
                ft.Radio(value="middle", label="中"),
                ft.Radio(value="right", label="右"),
            ]
        )
    )

    enbale_countdown_line = ft.Row(
        [
            ft.Checkbox(label="启用倒计时"),
            ft.TextField(label="倒计时", width=100),
        ],
    )

    send_command_button = ft.ElevatedButton(
        on_click=on_send_command_button_clicked,
        text="发送信息",
    )

    page.add(
        choose_color_line,
        choose_index_line,
        enbale_countdown_line,
        send_command_button,
    )


ft.app(target=main)
