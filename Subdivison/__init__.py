import logging

import azure.functions as func

import requests
from bs4 import BeautifulSoup
import io
import zipfile


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = req.params.get('url')  # Get the URL parameter from the request

    if url:
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

        # Create a zip file to store the PDF files
        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(in_memory_zip, 'w') as zip_file:
            # Download and add each PDF file to the zip file
            for file_name, download_link in file_links.items():
                response = requests.get(download_link)
                if response.status_code == 200:
                    file_content = response.content
                    zip_file.writestr(file_name, file_content)

        # Return the zip file as the response
        in_memory_zip.seek(0)  # Reset the pointer to the beginning of the file
        return func.HttpResponse(body=in_memory_zip.read(), status_code=200, headers={'Content-Type': 'application/zip', 'Content-Disposition': 'attachment;filename=scraped_files.zip'})

    else:
        return func.HttpResponse(
            "Please provide a 'url' parameter in the query string.",
            status_code=400
        )