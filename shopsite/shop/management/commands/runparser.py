from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from shop.models import Shop_item


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = parser()
        for i in range(len(data['names'])):
            Shop_item.objects.create(image_links=data['images'][i], name=data['names'][i], cost=data['prices'][i], description=data['description'][i])


def parser(pages=2):
    IMAGES = []
    NAMES = []
    PRICES = []
    DESCRIPTIONS = []

    #  Юзер-агент
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
              }

    #  url сайта
    url = 'https://catalog-sadovod.ru/novinki/?page='

    pages = pages  # Количество страниц для парсинга


    # Запрос
    for i in range(1, pages+1):
        try:
            print(f'Начата обработка страницы {i}')
            result = requests.get(url + str(i))

            soup = BeautifulSoup(result.text, "html.parser")

            items = soup.find_all('div', class_='ut2-gl__item')
            length = len(items)
            count = 0

            for item in items:
                count += 1
                print(f'Процесс обработки: {count/length*100:.2f}%')
                IMAGES.append(item.find('img').get('src'))
                NAMES.append(item.find('img').get('title'))
                PRICES.append(item.find('span', class_='ty-price-num').text + ' р')

                url_des = item.find('a', class_='ut2-quick-view-button cm-dialog-opener cm-tooltip cm-dialog-auto-size').get('href')
                result = requests.get(url_des)
                soup_des = BeautifulSoup(result.text, "html.parser")
                desc = soup_des.find(id='content_description').get_text()

                if desc == '\n':
                    DESCRIPTIONS.append('Продавец не предоставил описания товара.')
                else:
                    DESCRIPTIONS.append(desc)

        except: pass

    output = {'images': IMAGES, 'names': NAMES, 'prices': PRICES, 'description': DESCRIPTIONS}

    return output


