from bs4 import BeautifulSoup
import requests


def get_image():
    try:
        req = requests.get('http://photography.nationalgeographic.com/photography/photo-of-the-day/?source=fophotoright1')
    except requests.ConnectionError:
        raise ValueError("Failed to connect to natioanl geographic website")
    else:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        return 'http://'+soup.find('div', class_='primary_photo').find('img')['src'][2:]
