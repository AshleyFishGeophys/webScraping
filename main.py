from functions import scrape, extract, store, read, send_email

URL = "https://programmer100.pythonanywhere.com/tours/"

while True:
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="Hey new event was found!")
time.sleep(2)