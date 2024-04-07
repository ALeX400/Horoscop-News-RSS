import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
from urllib.parse import unquote
from datetime import datetime
import pytz

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
        'atom': "http://www.w3.org/2005/Atom",
        'content': "http://purl.org/rss/1.0/modules/content/",
        'wfw': "http://wellformedweb.org/CommentAPI/",
        'dc': "http://purl.org/dc/elements/1.1/",
        'sy': "http://purl.org/rss/1.0/modules/syndication/",
        'slash': "http://purl.org/rss/1.0/modules/slash/"
    }
    rss = etree.Element('rss', nsmap=nsmap, version="2.0")
    channel = etree.SubElement(rss, 'channel')

    # Adăugăm titlul de ansamblu, legătura atom, descrierea și alte detalii la channel
    title = etree.SubElement(channel, 'title')
    title.text = "Horoscop Zilnic – Horoscopul zilei de azi & Informatii Zodii"

    atom_link = etree.SubElement(channel, '{http://www.w3.org/2005/Atom}link', href="https://www.horoscop.ro/feed/", rel="self", type="application/rss+xml")

    link = etree.SubElement(channel, 'link')
    link.text = "https://www.horoscop.ro"

    description = etree.SubElement(channel, 'description')
    description.text = "Horoscop.ro - Urmărește zilnic horoscopul!"

    # Setăm lastBuildDate la data și ora curentă
    lastBuildDate = etree.SubElement(channel, 'lastBuildDate')
    now = datetime.now(pytz.utc)  # Folosim UTC pentru a fi consistent
    lastBuildDate.text = now.strftime('%a, %d %b %Y %H:%M:%S %z')

    language = etree.SubElement(channel, 'language')
    language.text = "ro-RO"

    updatePeriod = etree.SubElement(channel, '{http://purl.org/rss/1.0/modules/syndication/}updatePeriod')
    updatePeriod.text = "hourly"

    updateFrequency = etree.SubElement(channel, '{http://purl.org/rss/1.0/modules/syndication/}updateFrequency')
    updateFrequency.text = "1"

    # Adăugăm articolele
    for article in articles:
        item = etree.SubElement(channel, 'item')
        item_title = etree.SubElement(item, 'title')
        item_title.text = article['title']
        item_link = etree.SubElement(item, 'link')
        item_link.text = article['url']
        item_description = etree.SubElement(item, 'description')
        item_description.text = etree.CDATA(f'<img src="{unquote(article["image_url"])}" /><p>{article["summary"]}</p>{article["content"]}')

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
