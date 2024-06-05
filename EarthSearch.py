import os
import random
import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse



print("""
███████╗░█████╗░██████╗░████████╗██╗░░██╗░██████╗███████╗░█████╗░██████╗░░█████╗░██╗░░██╗
██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║░░██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║
█████╗░░███████║██████╔╝░░░██║░░░███████║╚█████╗░█████╗░░███████║██████╔╝██║░░╚═╝███████║
██╔══╝░░██╔══██║██╔══██╗░░░██║░░░██╔══██║░╚═══██╗██╔══╝░░██╔══██║██╔══██╗██║░░██╗██╔══██║
███████╗██║░░██║██║░░██║░░░██║░░░██║░░██║██████╔╝███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝""")
print("-------------------------------------------------------------------------------------------")

print("                       Github: https://github.com/MacPacS")

print("                               Version: 0.5.1")

print("-------------------------------------------------------------------------------------------")





# Function to generate a random folder name
def generate_random_folder_name(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for i in range(length))

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

def save_file(content, path):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    try:
        with open(path, 'wb') as file:
            file.write(content)
        print(f"Saved {path}")
    except IOError as e:
        print(f"Error saving file: {e}")

def download_resource(url, download_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
        parsed_url = urlparse(url)
        resource_path = os.path.join(download_folder, os.path.basename(parsed_url.path))
        save_file(response.content, resource_path)
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def extract_and_download_resources(soup, base_url, download_folder):
    os.makedirs(download_folder, exist_ok=True)
    
    # Save the HTML file
    html_file_path = os.path.join(download_folder, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print(f"HTML saved as {html_file_path}")
    
    # File extensions to consider for downloading
    resource_extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.php', '.asp', '.aspx', '.jsp']

    # Download linked resources
    for tag in soup.find_all(['link', 'script', 'img', 'a'], src=True):
        resource_url = tag.get('href') or tag.get('src')
        if resource_url:
            resource_url = urljoin(base_url, resource_url)
            parsed_url = urlparse(resource_url)
            extension = os.path.splitext(parsed_url.path)[1].lower()
            if extension in resource_extensions:
                download_resource(resource_url, download_folder)

def main():
    url = input("Please enter the website URL: ")
    html_content = fetch_webpage(url)
    
    if html_content:
        soup = parse_html(html_content)
        random_folder_name = generate_random_folder_name()
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads", random_folder_name)
        extract_and_download_resources(soup, url, download_folder)

if __name__ == "__main__":
    main()
