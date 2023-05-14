import requests
import selectorlib
import ssl
import os
import smtplib
import time
import sqlite3

# URL where I continuously fetch data
URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Establish a connection to the sqlite3 db
connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", (band, city, date))
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows


def send_email(subject, message, extracted_value):
    host = "smtp.gmail.com"
    port = 465

    username = "ashleymfish@gmail.com"
    password = os.getenv("PASSWORD")

    receiver = "ashleymfish@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        print("Logged in successfully")
        subject_line = f"New event found: {extracted_value}"
        email_message = f"{message}\n\nHere's the event: {extracted_value}"
        server.sendmail(username, receiver, f"Subject: {subject_line}\n\n{email_message}")
        print("Email sent successfully")


if __name__ == "__main__":
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
