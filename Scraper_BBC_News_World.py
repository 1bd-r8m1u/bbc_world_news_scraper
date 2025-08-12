import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# BBC News "World" section
url = "https://www.bbc.co.uk/news/world"

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Get HTML content
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch page:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Grab headlines from h3 tags
headlines = []
for h3 in soup.select("h3"):
    text = h3.get_text(strip=True)
    if text and len(text) > 15:  # Filter out short/non-headline text
        a_tag = h3.find_parent("a")
        if a_tag and a_tag.get("href"):
            link = a_tag["href"]
            if link.startswith("/"):  # Convert relative URLs
                link = "https://www.bbc.co.uk" + link
            headlines.append((text, link))

# Output to console
print("BBC News Headlines (World Section):")
for i, (title, link) in enumerate(headlines, start=1):
    print(f"{i}. {title}\n   {link}")

# Save to log file with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"logs/bbc_world_headlines_{timestamp}.txt"

with open(log_file, "w", encoding="utf-8") as f:
    for i, (title, link) in enumerate(headlines, start=1):
        f.write(f"{i}. {title}\n{link}\n\n")

print(f"\nSaved {len(headlines)} headlines to {log_file}")
