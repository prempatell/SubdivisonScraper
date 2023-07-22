import requests
from bs4 import BeautifulSoup
import os
import sys
import spacy

# Load the pre-trained language model
nlp = spacy.load("en_core_web_sm")

url = "https://plc.halifax.ca/hfxprod/pub/lms/Default.aspx?PossePresentation=ReferralResponse&PosseObjectId=25666994&AuthorizationKey=PFQYUFYGRECEFUCEFFYCNRRZAPNDDJDK"  # Replace with the actual URL
#url = sys.argv[1]

sudivision_path = r"C:\Users\premh\OneDrive - Province of Nova Scotia\Permit Docs\Subdivisons"
#sudivision_path = sys.argv[2]
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")



file_links = {}

def extract_entities(text):
    # Process the input text using SpaCy
    doc = nlp(text)
    
    # List to store the extracted entities
    entities_dict = {"PERSON": [], "EMAIL": [], "PHONE": []}
    
   # Loop through the named entities recognized by SpaCy
    for ent in doc.ents:
        # Filter entities of specific types (PERSON, EMAIL, PHONE)
        if ent.label_ in entities_dict:
            entities_dict[ent.label_].append(ent.text)
    
    return entities_dict

def metadata():
    referral_type = soup.find("span", id=lambda value: value and value.startswith("ReferralType")).text.strip()
    request_sent_date = soup.find("span", id=lambda value: value and value.startswith("RequestSentDate")).text.strip()
    referral_number = soup.find("span", id=lambda value: value and value.startswith("ReferralNumber")).text.strip()
    response_due_date = soup.find("span", id=lambda value: value and value.startswith("ResponseDueDate")).text.strip()
    reference_number = soup.find("span", id=lambda value: value and value.startswith("ReferenceNumber")).text.strip()
    organization_name = soup.find("span", id=lambda value: value and value.startswith("OrganizationName")).text.strip()
    status = soup.find("span", id=lambda value: value and value.startswith("PublicStatus")).text.strip()
    recipient_list = soup.find("span", id=lambda value: value and value.startswith("RecipientList")).text.strip()
    date_completed = soup.find("span", id=lambda value: value and value.startswith("DateCompleted")).text.strip()
    referral_text = soup.find("span", id=lambda value: value and value.startswith("ReferralText")).text.strip()
    referral_description = soup.find("span", id=lambda value: value and value.startswith("ReferralDescription")).text.strip()
    # Remove newlines and carriage returns from the referral description
    referral_description = referral_description.replace('\r', '').replace('\n', '')
    entities = extract_entities(referral_description)
    # Create a dictionary to store the scraped data
    scraped_data = {
        "ReferralType": referral_type,
        "RequestSentDate": request_sent_date,
        "ReferralNumber": referral_number,
        "ResponseDueDate": response_due_date,
        "ReferenceNumber": reference_number,
        "OrganizationName": organization_name,
        "Status": status,
        "RecipientList": recipient_list,
        "DateCompleted": date_completed,
        "Department Contact":entities["PERSON"],
        "Contact Phone":entities["PHONE"],
        "Contact Email":entities["EMAIL"],
        "ReferralText": referral_text,
        "ReferralDescription": referral_description,
        "Link": url
    }
    
    print( scraped_data)

for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.startswith("download.aspx"):
        file_name = link.text.strip()
        download_link = "https://plc.halifax.ca/hfxprod/pub/lms/" + href
        if file_name.endswith(".pdf") and download_link:
            file_links[file_name] = download_link

# Printing the filtered file names and download links
# for file_name, download_link in file_links.items():
#     # print("File Name:", file_name)
#     # print("Download Link:", download_link)
#     # print()

# Downloading the PDF files
for file_name, download_link in file_links.items():
    response = requests.get(download_link)
    if response.status_code == 200:
        file_path = os.path.join(sudivision_path, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        #print("Downloaded:", file_name)
    else:
        None
        #print("Failed to download:", file_name)

# print("All files downloaded successfully.")
# print(sudivision_path)
metadata()
# Test the function

