import requests
from bs4 import BeautifulSoup
from news.models import News


URLS = [
    "https://www.news18.com/tech/",
    "https://www.news18.com/politics/",
    "https://www.news18.com/india/",
    "https://www.news18.com/auto/",
    "https://www.news18.com/buzz/",
    "https://www.news18.com/entertainment/"
]


def news18_get_news_list(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find("div", {'class': 'section-blog-left-img-list'})
    ul = div.find("ul")
    list_items = ul.find_all("li")

    possible_categories = ["tech", "politics",
                           "india", "auto", "buzz", "entertainment"]

    category = ""

    for this_category in possible_categories:
        if this_category in URL:
            category = this_category

    news_list = []
    for item in list_items:
        news = {
            "url": str(item.find("a").get("href")),
            "title": str(item.find("a").text),
            "category": category
        }
        news_list.append(news)
    return news_list


def news18_get_news(news):

    r = requests.get(news["url"])
    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find("div", {'id': 'article_body'})

    paragraphs = div.find_all("p")

    paragraph_list = []
    for paragraph in paragraphs:
        paragraph_list.append(paragraph.text)

    # Image found
    image_div = soup.find("div", {'class': 'articleimg'})
    image = image_div.find(
        "picture").find("img").get("srcset")

    already = News.objects.filter(title=news["title"])

    body = ""

    for paragraph in paragraph_list:
        body += paragraph.replace("\n", "") + "\n\n"
    if not already:
        description = body[0:150]
        this_news = News.objects.create(
            title=news["title"], description=description, body=body, image=image, category=news["category"])
        this_news.save()
    else:
        print("Now already exist")


def news18_generate():
    for URL in URLS:
        for news in news18_get_news_list(URL):
            news18_get_news(news)
