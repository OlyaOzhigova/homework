import requests
from bs4 import BeautifulSoup

# ключевые слова для поиска
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def fetch_articles():
    url = 'https://habr.com/ru/articles/'

    response = requests.get(url)
    response.raise_for_status()  # успешно?

    # парсим страницу
    soup = BeautifulSoup(response.text, 'lxml')

    # находим статьи
    articles_list = soup.findAll('div', class_='tm-article-snippet')

    # список, который будем наполнять нужными статьями
    matching_articles = []

    # Обрабатываем каждую статью
    for article in articles_list:
        link = f"https://habr.com{article.find('a', class_='tm-title__link')['href']}"

        # ссылка
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, 'lxml')

        # заголовок, дата
        title = article_soup.find('h1').text.strip()
        time = article_soup.find('time')['datetime']

        # извлекаем текст
        text_div = article_soup.find('div', class_='article-formatted-body')
        if text_div:
            text = text_div.get_text(strip=True, separator=' ')
        else:
            text = ''

        # проверяем, есть ли ключевые слова в заголовке или тексте
        if any(keyword.lower() in (title.lower() + ' ' + text.lower()) for keyword in KEYWORDS):
            #вывод всех переменных + текст
            # matching_articles.append(f"{time} – {title} – {link} – {text[:200]}...")

            # вывод <дата> – <заголовок> – <ссылка>
            matching_articles.append({
                'data':time,
                'title':title,
                'link':link
            })
    return matching_articles


if __name__ == '__main__':
    articles = fetch_articles()
    for article in articles:
        print(article)