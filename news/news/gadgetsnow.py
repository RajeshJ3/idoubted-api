import requests
from bs4 import BeautifulSoup
from news.models import News

URL = "https://www.gadgetsnow.com/jobs"


URLS = [
    "https://www.gadgetsnow.com/tech-news",
    "https://www.gadgetsnow.com/jobs",
    "https://www.gadgetsnow.com/it-services",
    "https://www.gadgetsnow.com/social",
    "https://www.gadgetsnow.com/mobiles",
    "https://www.gadgetsnow.com/pcs",
    "https://www.gadgetsnow.com/apps",
    "https://www.gadgetsnow.com/gaming",
    "https://www.gadgetsnow.com/computing",
    "https://www.gadgetsnow.com/who-is",
    "https://www.gadgetsnow.com/more-gadgets",
]


def gadgetsnow_get_news_list(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find("div", {'id': 'c_wdt_list_1'})
    ul = div.find("ul", {'class': 'cvs_wdt'})
    list_items = ul.find_all("li")

    possible_categories = ["tech-news", "jobs",
                           "it-services", "social", "mobiles", "pcs", "apps", "gaming", "computing", "who-is", "more-gadgets"]

    category = ""
    for this_category in possible_categories:
        if this_category in URL:
            category = this_category
    if category == "tech-news":
        category = "tech"

    news_list = []
    for item in list_items:
        title = item.find("span", {'class', 'w_tle'})
        image = item.find("a", {'class', 'w_img'}).find("img").get("data-src")
        description = item.find("span", {'class', 'w_desc'})

        news = {
            "url": str(title.find("a").get("href")),
            "title": str(title.text),
            "description": str(description.text),
            "category": category
        }
        news_list.append(news)
    return news_list


def gadgetsnow_get_news(news):
    r = requests.get(URL+news["url"])
    soup = BeautifulSoup(r.text, "html.parser")

    if len(soup.find_all("div", {'id': 'c_as_wdt_content_2'})) == 0:
        print("Skipped: " + news["title"])
        return False

    div = soup.find("div", {'class': 'section1'})

    paragraphs = str(div.text)

    paragraph_list = paragraphs.split("\n\n")

    # Image
    highligh = soup.find("section", {'class': 'highlight clearfix'})
    if len(highligh.find_all("div", {'class': 'highlight_img'})) == 0:
        print("Skipped: " + news["title"])
        return False
    image_div = highligh.find("div", {'class': 'highlight_img'})
    image = image_div.find("img").get("src")

    already = News.objects.filter(title=news["title"])

    body = ""
    for paragraph in paragraph_list:
        body += paragraph.replace("\n", "") + "\n\n"

    if not already:
        this_news = News.objects.create(
            title=news["title"], description=news["description"], body=body, image=image, category=news["category"])
        this_news.save()
        print("Added: " + news["title"])
    else:
        print("Now already exist")


def gadgetsnow_generate():
    for URL in URLS:
        for news in gadgetsnow_get_news_list(URL):
            if "https://www.gadgetsnow.com/slideshows/" in news["url"] or "This article is no longer available" in news["title"]:
                continue
            gadgetsnow_get_news(news)
