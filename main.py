import flet as ft
import parser_dns
import json


def main(page: ft.Page):
    def refresh_data(e):
        pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
        container_1.content = pr
        bt.disabled = True
        page.update()
        global data, keys_gadgets
        data = parser_dns.parser()
        keys_gadgets = list(data['gadgets'].keys())
        container_1.content = None
        bt.disabled = False
        images.controls = []
        add_images(images)
        page.update()

    page.window_width = 665
    page.window_height = 770
    container_1 = ft.Container(
    )
    bt = ft.FilledButton(text='Обновить данные',
                         width=600,
                         on_click=refresh_data
                         )
    page.add(ft.Row([bt, container_1]))

    def dropdown_changed(e):
        if dd.value == 'По возрастанию цены':
            keys_gadgets.sort(key=lambda x: data['gadgets'][x]['price']['current'] if not 'min' in data['gadgets'][x]['price'] else data['gadgets'][x]['price']['min'])
        else:
            keys_gadgets.sort(key=lambda x: data['gadgets'][x]['price']['current'] if not 'min' in data['gadgets'][x]['price'] else data['gadgets'][x]['price']['min'], reverse=True)
        images.controls = []
        add_images(images)
        page.update()
    dd = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("По возрастанию цены"),
            ft.dropdown.Option("По убыванию цены"),
        ],
        width=300,
        hint_text='Сортировка',
    )
    page.add(dd)
    images = ft.Column(expand=1, wrap=False, scroll="always")

    def add_images(images):
        for idx, i in enumerate(keys_gadgets):

            price = data['gadgets'][i]['price']
            current = price['current']
            min_price = '99999999'
            if 'min' in price:
                min_price = price['min']

            images.controls.append(
                ft.Row(
                    [ft.Container(
                        image_src=data['gadgets'][i]['img_url'],
                        width=200,
                        height=200,
                        border_radius=ft.border_radius.all(10),
                        url=data['gadgets'][i]['url']
                    ), ft.Column(
                        [ft.Container(content=ft.Text(data['gadgets'][i]['character'], width=400, size=17),
                                      height=120),
                         ft.Text(
                             f'{min(int(current), int(min_price))} ₽',
                             size=30
                         )
                         ]
                    )
                    ]
                )
            )

    add_images(images)
    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[]
    )

    page.add(images)


if __name__ == '__main__':
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    keys_gadgets = list(data['gadgets'].keys())
    print(keys_gadgets)
    ft.app(target=main)
