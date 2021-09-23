import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST='https://www.mashina.kg'
URL='https://www.mashina.kg/search/honda/all/'
HEADERS={
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}


def get_html(url, params=''):
    r=requests.get(url,headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list-item list-label')
    cards = []
    print(items)
    for item in items:
        cards.append(
            {
                'title':item.find('h2',class_='name').get_text(strip=True),# strip=True убрать пробелы
                'product_link': HOST+item.find('a').get('href'),
                'price': item.find('p', class_='price').find('strong').get_text(strip=True),
                'card_img': item.find('img', class_='lazy-image')['data-src'],

            }
        )
    return cards

# html = get_html(URL)
# print(html)
# cards = get_content(html.text)
# for i in cards:
#     print(i)



def save_doc(items,path):
    with open(path,'w',newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(['название машины','ссылка на детализацию','Цена','Картинка'])
        for item in items:
            writer.writerow([  item['title'], item['product_link'], item['price'], item['card_img'] ])


def parser():
    PAGINATION = input('Укажите количество страниц для парсинга:')
    PAGINATION=int(PAGINATION.strip())   # .strip() если пользователь ввел пробелы то мы убераем. Данные преобразуем в целочисленный тип
    html = get_html(URL)
    if html.status_code == 200: # если сервер вернет код 200, значит все работает хорошо
        cards = []
        for page in range(PAGINATION):
            print(f'Идет процесс сборки данных страницы: {page}')
            html = get_html(URL, params={'page':page}) # params то что меняется в url сайта
            cards.extend(get_content(html.text))
            save_doc(cards,CSV)
        print(cards)
    else:
        print('Error')

parser()

