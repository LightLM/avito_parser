import time
import requests
from bs4 import BeautifulSoup
import json
from settings import *


def parser():
    root_dict = {'gadgets': {}}
    dict_data = {"type": "product-buy", "containers": []}
    l_checker = []
    while int(params['p']) < 99:
        response = requests.get(
            'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_="catalog-product ui-button-widget")
        if not products:
            print('Ноуты закончились')
            break
        # print(len(products))
        for i in products:
            id_num = i['data-code']
            name_book = i.find('img')['alt']
            id_letter = i.find('span', class_="catalog-product__buy product-buy")['id']
            url_img = i.find('source')['data-srcset']
            url_book = 'https://www.dns-shop.ru' + i.find('a', class_="catalog-product__image-link")['href']
            text_book = i.find('a', class_="catalog-product__name ui-link ui-link_black").text

            dict_data['containers'].append({'id': id_letter, 'data': {"id": id_num}})

            l_checker.append([id_num, name_book, id_letter, url_img, url_book, text_book])
            print(len(l_checker))
            print(l_checker[-1])

            root_dict['gadgets'][id_num] = {'name': name_book, 'img_url': url_img, 'url': url_book,
                                            'character': text_book}
            # print(i['data-code'])
            # print(i.find('img')['alt'])
            # print(i.find('span', class_="catalog-product__buy product-buy")['id'])
            # print(i.find('source')['data-srcset'])
            # print('\n')
        params['p'] = str(int(params['p']) + 1)
        time.sleep(2)

    data = f'data={dict_data}'
    data = data.replace("'", '"')

    response = requests.post('https://www.dns-shop.ru/ajax-state/product-buy/', cookies=cookies_for_post,
                             headers=headers_for_post, data=data)

    keys_gadgets = list(root_dict['gadgets'].keys())
    print(len(keys_gadgets))
    for idx, i in enumerate(response.json()['data']['states']):
        root_dict['gadgets'][keys_gadgets[idx]]['price'] = i['data']['price']

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(root_dict, file, ensure_ascii=False)
    print(root_dict)


if __name__ == '__main__':
    parser()
