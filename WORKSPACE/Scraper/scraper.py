import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Optional
from datetime import datetime
import time
import random

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def extract_data(self, soup: BeautifulSoup) -> List[Dict]:
        if not soup:
            return []
        
        # Example: extracting all article titles, links, and additional metadata
        articles = []
        for article in soup.find_all(['article', 'div.post', 'div.article']):
            data = {}
            
            # Title and link
            title_elem = article.find(['h1', 'h2', 'h3'])
            if title_elem:
                data['title'] = title_elem.text.strip()
                link = title_elem.find('a')
                if link:
                    data['url'] = link.get('href', '')
                    if data['url'].startswith('/'):
                        data['url'] = f"{self.base_url.rstrip('/')}{data['url']}"
            
            # Date/timestamp if available
            date_elem = article.find(class_=['date', 'time', 'timestamp'])
            if date_elem:
                data['date'] = date_elem.text.strip()
            
            # Description/excerpt if available
            desc_elem = article.find(class_=['description', 'excerpt', 'summary'])
            if desc_elem:
                data['description'] = desc_elem.text.strip()
            
            # Author if available
            author_elem = article.find(class_=['author', 'byline'])
            if author_elem:
                data['author'] = author_elem.text.strip()
            
            if data.get('title'):  # Only add if at least title was found
                data['scraped_at'] = datetime.now().isoformat()
                articles.append(data)
        
        return articles

    def save_to_json(self, data: List[Dict], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    # Example usage: scraping a news website
    scraper = WebScraper('https://example.com')
    soup = scraper.fetch_page(scraper.base_url)
    
    if soup:
        data = scraper.extract_data(soup)
        scraper.save_to_json(data, 'scraped_data.json')
        print(f"Successfully scraped {len(data)} items")
    else:
        print("Failed to fetch the page")

if __name__ == "__main__":
    main()