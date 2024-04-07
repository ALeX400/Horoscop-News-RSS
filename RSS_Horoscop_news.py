import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
from urllib.parse import unquote

def fetch_article_details(article_url):
    try:
        response = requests.get(article_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('div', class_='title-wrapper').h1.text
            summary = soup.find('div', class_='autor-data').find_next_sibling().text
            image_url = soup.find('div', class_='thumb').img['src']
            # Asigurăm că URL-ul imaginii este decodificat
            image_url = unquote(image_url)

            # Eliminăm elementele 'banner-aside'
            for banner_aside in soup.find_all('div', class_='banner-aside'):
                banner_aside.decompose()

            # Concatenăm conținutul de interes
            content = str(soup.find('section', class_='article-intro')) + str(soup.find('div', class_='__content'))

            return title, summary, image_url, content
    except Exception as e:
        print(f"Failed to fetch article details: {e}")
    return None, None, None, None

def construct_rss_feed(articles):
    nsmap = {
        'content': "http://purl.org/rss/1.0/modules/content/",
        'wfw': "http://wellformedweb.org/CommentAPI/",
        'dc': "http://purl.org/dc/elements/1.1/",
        'atom': "http://www.w3.org/2005/Atom",
        'sy': "http://purl.org/rss/1.0/modules/syndication/",
        'slash': "http://purl.org/rss/1.0/modules/slash/"
    }
    rss = etree.Element('rss', nsmap=nsmap, version="2.0")
    channel = etree.SubElement(rss, 'channel')

    for article in articles:
        item = etree.SubElement(channel, 'item')
        title = etree.SubElement(item, 'title')
        title.text = article['title']
        link = etree.SubElement(item, 'link')
        link.text = article['url']
        description = etree.SubElement(item, 'description')
        # Construim CDATA cu URL-ul decodificat și restul conținutului
        description_content = f'<img src="{article["image_url"]}" /><p>{article["summary"]}</p>{article["content"]}'
        description.text = etree.CDATA(description_content)

    return etree.tostring(rss, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def main():
    feed_url = 'https://spynews.ro/horoscop/'
    response = requests.get(feed_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        listing_column = soup.find('div', class_="listing-column")
        articles = listing_column.find_all('a', class_='news-item')

        articles_data = []
        for article in articles[:5]:  # Limităm la primele 5 articole
            article_url = article['href']
            title, summary, image_url, content = fetch_article_details(article_url)
            if title:
                articles_data.append({
                    'title': title,
                    'summary': summary,
                    'image_url': image_url,
                    'content': content,
                    'url': article_url
                })

        rss_content = construct_rss_feed(articles_data)
        os.makedirs('docs', exist_ok=True)
        with open('docs/horoscop_news.xml', 'wb') as file:
            file.write(rss_content)
        print("RSS feed created successfully.")
    else:
        print("Failed to fetch horoscope news.")

if __name__ == "__main__":
    main()
