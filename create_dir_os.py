from saver import *


def create_holiday_dir_with_img(theme_url):
    """
    Создаёт папки с названиями праздников и сохраняет в них соответствующие файлы
    :param date_list: Уникальные названия дат в листе (list)
    :return: None
    """
    titles = []
    cards_urls = []

    start_url = f'{theme_url}page-1/'
    rq = requests.get(start_url)
    b_soup = BeautifulSoup(rq.text, 'html.parser')

    last_page = page_count(b_soup)

    for page_num in range(1, last_page + 1):
        """
        Проходится по всем страницам с текущими открытками, собирает: 
        названия праздников в titles,
        ссылки на открытки в card_urls
        """
        url = f'{theme_url}page-{page_num}'
        r1 = requests.get(url)
        soup = BeautifulSoup(r1.text, 'html.parser')

        titles_list = soup.find_all('strong')
        for title in titles_list:
            titles.append(title.text)

        cards = soup.find_all('a', {'class': 'card-image'})
        for card in cards:
            url = card.get('href')
            cards_urls.append(url)

    for holiday in titles:
        try:
            os.mkdir(holiday)
        except FileExistsError:
            pass
        os.chdir(holiday)
        save_imgs(cards_urls[titles.index(holiday)])
        print('//')
        os.chdir('..')


def del_empty_dirs(path):
    """
    Удаляет пустые папки в случае если такие образовались из-за присутствия в открытках только видео-формата
    Рекурсивная функция проходится по всем папкам начиная с директории path
    При удалении папки выводит в командной строке название удалённой папки
    :param path: Путь
    :return: None
    """
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
                print(a, 'удалена')


def run():
    for th in theme:
        if th == 'Топ открыток' or th == 'утро, день, вечер' or th == 'Календарь':
            pass
        else:
            try:
                os.mkdir(th)
            except FileExistsError:
                pass
            os.chdir(th)
            create_holiday_dir_with_img(theme_urls[theme.index(th)])
            del_empty_dirs(os.curdir)
            os.chdir('..')
            print(f'Тема {th} скачана')
    print('Загрузка завершена')

