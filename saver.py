import urllib.request
import os
from parser import *


def save_imgs(url):
    """
    Сохраняет все файлы формата jpg и gif в текущей директории,
    присваивая им порядковые номера начиная с 1.
    Видео-файлы пропускает.
    :param url: ссылка на тему
    :return: None
    """
    card_url = url
    r2 = requests.get(card_url)
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    last_page_img = page_count(soup2)
    img_urls = []
    if last_page_img > 1:
        for page_numb in range(1, last_page_img+1):
            r3 = requests.get(f'{card_url}/page-{page_numb}')
            soup3 = BeautifulSoup(r3.text, 'html.parser')

            card = soup3.find_all('div', {'class': 'card-image'})

            for card_img in card:
                img_urls.append(card_img.find('a').get('href'))
    else:
        card = soup2.find_all('div', {'class': 'card-image'})

        for card_img in card:
            img_urls.append(card_img.find('a').get('href'))

    name_ind = 1
    for img_url in img_urls:
        r4 = requests.get(img_url)
        soup4 = BeautifulSoup(r4.text, 'html.parser')
        file_url = soup4.find('div', {'id': 'card-image'})
        url_container = file_url.find('img', {'class': 'cardContent'})

        if url_container is None:
            pass
        else:
            img = url_container.get('src')
            img_name = f'{name_ind}{(str(img))[-4:]}'

            if os.path.exists(f'{os.getcwd()}/{img_name}'):
                print(end='!')
            else:
                urllib.request.urlretrieve(img, img_name)
                print(end='#')
            name_ind += 1

