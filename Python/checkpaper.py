import requests
from bs4 import BeautifulSoup

url = "https://zhentaoshi.github.io/papersbyyears/"
text_to_check = "Relaxed Balancing for Synthetic Control"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

linked = any(a for a in soup.find_all("a") if text_to_check in a.get_text())

if linked:
    print("Paper is now available!")
    exit(1)  # Trigger GitHub Action failure
else:
    print("Paper not yet uploaded.")
    exit(0)  # Normal exit, no notification
