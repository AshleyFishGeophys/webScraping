from functions import scrape, extract, store, read, send_email
import time

URL = "https://programmer100.pythonanywhere.com/tours/"

while True:
    scraped = scrape(URL)
    extracted = extract(scraped)
    print("extracted:", extracted)
    if extracted != "No upcoming tours":
        row = read(extracted)
        # Checks to see if event already exists in the table
        if not row:
            store(extracted)
            extracted_value = ", ".join(extracted.split(","))
            message = "Hey new event was found!"
            subject = "New event alert!"
            send_email(subject, message, extracted_value)
    time.sleep(2)