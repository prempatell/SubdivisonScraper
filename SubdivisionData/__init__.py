import logging
import json
import requests
from bs4 import BeautifulSoup
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = req.params.get('url')  # Get the URL parameter from the request

    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

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
            "ReferralText": referral_text,
            "ReferralDescription": referral_description
        }

        # Convert the dictionary to JSON
        json_data = json.dumps(scraped_data)

        # Return the JSON data as the response
        return func.HttpResponse(body=json_data, status_code=200, headers={'Content-Type': 'application/json'})

    else:
        return func.HttpResponse(
            "Please provide a 'url' parameter in the query string.",
            status_code=400
        )
