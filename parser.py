import requests
from bs4 import BeautifulSoup


base_url = 'https://3d-galleru.ru/'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, 'html.parser')


def page_count(b_soup):
    """
    Определяет количество страниц с информацией
    :param b_soup: объект BeautifulSoup
    :return: Количество страниц в формате int
    """
    pages = b_soup.find('div', {'id': 'pages'})
    if pages.text == '':
        last_page_find = 1
    else:
        all_pages = str(pages.text)
        if '123456...' in all_pages:
            last_page_find = all_pages[10:]
        else:
            last_page_find = all_pages[-1]
    return int(last_page_find)


theme = []
theme_urls = []


themes = soup.find('ul', {'id': 'chapter-menu'}).find_all('a')
for theme_name in themes:
    theme.append(theme_name.text)
    theme_urls.append(f"https://3d-galleru.ru{theme_name.get('href')}")

