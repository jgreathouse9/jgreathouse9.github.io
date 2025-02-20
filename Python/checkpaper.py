import requests
from bs4 import BeautifulSoup

url = "https://zhentaoshi.github.io/papersbyyears/"
text_to_check = "Relaxed Balancing for Synthetic Control"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Check if the text is hyperlinked
linked = any(a for a in soup.find_all("a") if text_to_check in a.get_text())

if linked:
    print("Paper is now available! Exiting with failure to trigger notification.")
    exit(1)  # Fail intentionally to trigger GitHub Actions email
else:
    print("Paper not yet uploaded. Exiting normally.")
    exit(0)  # Pass silently
