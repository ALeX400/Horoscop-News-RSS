import requests
import os

def save_rss_feed(feed_url, save_path):
    try:
        # Verifică și creează directorul dacă nu există
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        response = requests.get(feed_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("RSS feed salvat cu succes.")
        else:
            print(f"Eroare la solicitare: Status Code {response.status_code}")
    except Exception as e:
        print(f"Eroare la accesarea feed-ului RSS: {str(e)}")

# URL-ul de la care se extrage feed-ul RSS
feed_url = 'https://www.horoscop.ro/feed/'
# Calea unde va fi salvat fisierul XML
save_path = 'docs/index.xml'

save_rss_feed(feed_url, save_path)
