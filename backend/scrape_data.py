import requests
from bs4 import BeautifulSoup
from googlesearch import search
from pathlib import Path


def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        # print(f"Error fetching {url}: {e}")
        return None
    
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading/trailing whitespace on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
    
def write_text_to_file(url, text, index):
    directory = Path("input")
    directory.mkdir(parents=True, exist_ok=True)
    
    # Create a valid filename from the URL
    filename = directory / f"input_text_{index}.txt"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n\n{text}")
    # print(f"Written text to {filename}")
    
    
def search_and_extract_text(topic, num_results=10):
    unique_urls = set()  # Use a set to avoid duplicate URLs
    results = []
    
    for url in search(topic, lang="en", num_results=30):  # Fetch more results in one go
        if len(unique_urls) >= num_results:
            break
        if url not in unique_urls:
            unique_urls.add(url)
    
    index = 1
    for url in unique_urls:
        # print(f"Fetching content from: {url}")
        html_content = fetch_page_content(url)
        if html_content:
            text = extract_text_from_html(html_content)
            results.append((url, text))
            write_text_to_file(url, text, index)
            index += 1
    print("Scraping Done: ", unique_urls)
    return unique_urls