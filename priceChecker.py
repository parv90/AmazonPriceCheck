import requests
from bs4 import BeautifulSoup
import time
import smtplib

URL = 'https://www.amazon.in/HOBBIT-BATTLE-FIVE-ARMIES/dp/B07BZZD1YV/?_encoding=UTF8&pd_rd_w=xlRCm&pf_rd_p=fcac17e8-2a87-4225-8628-a80b57a1a106&pf_rd_r=8KC1BPWY91XSE2XTEXQJ&pd_rd_r=606976d5-43b6-4dec-b8dc-185a81bb5f61&pd_rd_wg=rTsDQ&ref_=pd_gw_cr_cartx'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

page =  requests.get(URL, headers=headers)
content = page.content

# create the soup object
soup = BeautifulSoup(page.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')

def check_price():
  title = soup.find(id = "productTitle").get_text()
  price = [i.get_text() for i in soup.find_all('span', {'class': 'a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P'})]
  price = soup.find(class_ = "price3P").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()

  converted_price = float(price[0:5])
  print(converted_price)
  print(title.strip())

  if converted_price < 342:
        send_email()

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('yourEmail', 'serverCode')

    subject = 'Price Fell Down!'
    body = f'Check the amazon link {URL}'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'yourEmail',
        'emailInWhichYouWantToSend',
        msg
    )

    print('Hey! email is send')
    
    server.quit()


check_price()