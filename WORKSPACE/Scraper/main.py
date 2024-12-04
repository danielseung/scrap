import argparse
from scraper import WebScraper
import sys
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Scraper CLI')
    parser.add_argument('url', help='The URL to scrape')
    parser.add_argument('-o', '--output', default='scraped_data.json',
                      help='Output JSON file name (default: scraped_data.json)')
    parser.add_argument('-p', '--pages', type=int, default=1,
                      help='Number of pages to scrape (default: 1)')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                      help='Delay between requests in seconds (default: 1.0)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        scraper = WebScraper(args.url)
        all_data = []
        
        print(f"Starting to scrape {args.pages} page(s) from {args.url}")
        
        for page in range(1, args.pages + 1):
            print(f"Scraping page {page}/{args.pages}")
            
            # Construct page URL (modify this according to the website's pagination pattern)
            page_url = f"{args.url}/page/{page}" if page > 1 else args.url
            
            soup = scraper.fetch_page(page_url)
            if soup:
                data = scraper.extract_data(soup)
                all_data.extend(data)
                print(f"Found {len(data)} items on page {page}")
                
                if page < args.pages:
                    print(f"Waiting {args.delay} seconds before next request...")
                    time.sleep(args.delay)
            else:
                print(f"Failed to fetch page {page}")
                break
        
        if all_data:
            scraper.save_to_json(all_data, args.output)
            print(f"\nScraped {len(all_data)} total items")
            print(f"Data saved to {args.output}")
        else:
            print("No data was scraped")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()