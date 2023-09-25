import time
import os
import base64
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build

# Custom packages
from google_api_auth import gmail
from google_api_auth.setup_logging import setup_logger

LOGGER = setup_logger('wodify')
WODIFY_LABEL = 'Label_31974612365702973'
WODIFY_EMAIL_BOOKING_CONTENT_DIV_ID = "wt11_wtTitle"
GMAIL_CREDENTIALS_PATH = os.environ.get('gmail_credentials_path', os.getcwd())

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def parse_html_for_booking_link(email_html):
    soup = BeautifulSoup(email_html, 'html.parser')
    anchor_tag = soup.findAll('a', href=True, string='Accept')[0]
    return anchor_tag['href']


def is_booking_email(email_content):
    if 'The class you wait-listed for is now open for reservation' in email_content:
        LOGGER.info('Booking email found - attempting booking')
        return True
    return False


def book_class(booking_url):
    resp = requests.get(booking_url)
    resp_soup = BeautifulSoup(resp.text, 'html.parser')
    div = resp_soup.find("div", {"id": WODIFY_EMAIL_BOOKING_CONTENT_DIV_ID})
    LOGGER.info(div.text.replace('\xa0', ''))


def is_new_email(email_id):
    email_id_file = 'email.txt'
    if os.path.isfile(email_id_file):
        with open('email.txt', 'r') as f:
            last_email_id = f.read()
        return email_id != last_email_id
    return False


def get_email_html(gmail_email_data):
    email_parts = gmail_email_data['payload']['parts']
    main_body = email_parts[1]['parts'][0]['body']['data']
    html = base64.urlsafe_b64decode(main_body).decode('utf-8')
    return html

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = gmail.get_token(GMAIL_CREDENTIALS_PATH, SCOPES)
    LOGGER.info('Proceeding with body of program')

    while True:
        try:
            service = build('gmail', 'v1', credentials=creds)
            response = service.users().messages().list(labelIds=[WODIFY_LABEL], userId='me').execute()
            most_recent_email_id = response['messages'][0]['id']

            if is_new_email(most_recent_email_id):
                LOGGER.info('New email - parsing to see if we can book')
                gmail_email_data = service.users().messages().get(id=most_recent_email_id, userId='me').execute()
                html_content = get_email_html(gmail_email_data)

                if is_booking_email:
                    booking_url = parse_html_for_booking_link(html_content)
                    book_class(booking_url)

            else:
                LOGGER.info('Email is the same as last time - nothing to do')

            with open('email.txt', 'w') as f:
                f.write(most_recent_email_id)

            time.sleep(1)

        except Exception as error:
            # TODO - Handle specific refresh token failure and call get_token again
            LOGGER.error(f'An error occurred: {error}')
            LOGGER.error('Sleeping for 10 seconds due to error')
            time.sleep(10)


if __name__ == '__main__':
    main()

