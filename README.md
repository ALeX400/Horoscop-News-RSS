
# Horoscope News Scraper and RSS Feed Generator

This Python script is designed to fetch the latest horoscope news from a specific URL, process the content, and generate an RSS feed. It utilizes libraries such as `requests` for fetching web content, `BeautifulSoup` for HTML parsing, `lxml` for XML manipulation, and `tqdm` for displaying progress bars. This tool is perfect for anyone looking to automate the creation of an RSS feed for horoscope-related content.

## Features

- Fetches latest horoscope news from a predefined URL.
- Parses HTML content to extract relevant article details (title, summary, image URL, and content).
- Cleans up the content by removing unwanted sections and formatting issues.
- Generates an RSS feed with the extracted content, including article titles, summaries, image URLs, and formatted content.
- Utilizes `tqdm` to display a progress bar during the fetching and processing of articles.
- Handles cases where content might be dynamically formatted or include additional sections like "Citește și:".

## Dependencies

- `requests`: For making HTTP requests to fetch web content.
- `BeautifulSoup`: For parsing HTML and extracting necessary data.
- `lxml`: For generating and manipulating the RSS feed in XML format.
- `pytz`: For handling time zone information in date and time operations.
- `tqdm`: For displaying progress bars to the console.
- `re`: For regular expressions used in content cleanup.
- `os`: For file and directory operations.
- `urllib.parse`: For URL parsing and manipulation.

## How to Use

1. Ensure all dependencies are installed:
   ```bash
   pip install requests beautifulsoup4 lxml pytz tqdm
   ```

2. Save the script to a local file, for example, `horoscope_rss_generator.py`.

3. Run the script:
   ```bash
   python horoscope_rss_generator.py
   ```

4. The script will fetch the latest articles, process them, and generate an RSS feed in the `docs/horoscop_news.xml` file.

## Customization

- The script can be customized to fetch articles from different sections or websites by modifying the `feed_url` variable and adjusting the parsing logic in the `fetch_article_details` function.
- The RSS feed's overall structure and metadata can be customized in the `construct_rss_feed` function.

## Note

This script is designed for educational purposes and to demonstrate web scraping, content processing, and RSS feed generation with Python. Ensure you have the right to scrape and reuse the content from the target website.
