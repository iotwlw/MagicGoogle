import logging

# Define some constants


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
URL_FIRST = "https://{domain}/search?q={query}&qs=bs&ajf=60&FORM=QBLH"
URL_NEXT = "https://{domain}/search?q={query}&qs=bs&ajf=60&first={first}&FORM=PORE"

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('magic_google')
