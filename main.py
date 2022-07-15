import requests
from bs4 import BeautifulSoup


def article_search():
    BASE_URL = 'https://habr.com'
    URL = BASE_URL + '/ru/all/'

    # определяем список ключевых слов
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    # создаем лже-заголовок для запроса
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Cookie': 'hl=ru; fl=ru; _ym_uid=1651856558735804488; _ym_d=1651856558; _ga=GA1.2.64404454.1651856560; '
                  'visited_articles=485236; habr_web_home_feed=/all/; _gid=GA1.2.1213157240.1657374839; _ym_isad=2',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    # получаем страницу с самыми свежими постами
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, features='html.parser')

    # извлекаем превью статей
    articles = soup.find_all('article', class_='tm-articles-list__item')
    for article in articles:

        # получаем полный текст статей
        response = requests.get(BASE_URL + article.find(class_='tm-article-snippet__title-link').attrs.get('href'),
                                headers=HEADERS)
        soup = BeautifulSoup(response.text, features='html.parser')
        full_articles = soup.find_all('div', xmlns='http://www.w3.org/1999/xhtml')
        full_articles = [item.text.strip() for item in full_articles]

        # ищем вхождения, необходимых, ключевых слов
        # и выводим (дата - заголовок - ссылка) статей,
        # удовлетворяющих запросу
        for full_article in full_articles:
            i = 0
            while i < len(KEYWORDS):
                if KEYWORDS[i] in full_article:
                    href = BASE_URL + article.find(class_="tm-article-snippet__title-link").attrs.get("href")
                    title = article.find('h2').find('span').text
                    date = article.find(class_='tm-article-snippet__datetime-published').find("time").attrs.get("title")
                    print(date, '-', title, '-', href)
                i += 1


if __name__ == '__main__':
    article_search()