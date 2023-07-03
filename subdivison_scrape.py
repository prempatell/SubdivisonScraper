import requests
from bs4 import BeautifulSoup
import os

url = "https://plc.halifax.ca/hfxprod/pub/lms/Default.aspx?PossePresentation=ReferralResponse&PosseObjectId=25666994&AuthorizationKey=PFQYUFYGRECEFUCEFFYCNRRZAPNDDJDK"  # Replace with the actual URL
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

file_links = {}

for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.startswith("download.aspx"):
        file_name = link.text.strip()
        download_link = "https://plc.halifax.ca/hfxprod/pub/lms/" + href
        if file_name.endswith(".pdf") and download_link:
            file_links[file_name] = download_link

# Printing the filtered file names and download links
for file_name, download_link in file_links.items():
    print("File Name:", file_name)
    print("Download Link:", download_link)
    print()

# Downloading the PDF files
for file_name, download_link in file_links.items():
    response = requests.get(download_link)
    if response.status_code == 200:
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("Downloaded:", file_name)
    else:
        print("Failed to download:", file_name)

print("All files downloaded successfully.")
