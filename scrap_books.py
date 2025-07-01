import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = 'https://books.toscrape.com/'

user = input('What would be your preffered rating?').capitalize()

response = requests.get(base_url)
response.encoding='utf-8'
content = response.text

soup = BeautifulSoup(content, 'html.parser')
books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

count = 0

for book in books:
    
    book_name = book.find('h3').find('a')['title']
    rating_class = book.find('p', class_='star-rating')['class']
    book_rating = rating_class[1] 
    book_info = book.find('a')['href']
    link_ = urljoin(base_url,book_info )
    if user == book_rating:
        count = count + 1
        price = book.find('p', class_ = 'price_color').text.replace(" ","")
        price_text = price.strip().replace('£', '')
        price = float(price_text)

        if price > 50:
            print([count])
            print(f"Expensive book: {book_name} - £{price}")
            print(f"Rating: {book_rating}")
            print(link_)
        else:
            print([count])
            print(f"Cheap book: {book_name} - £{price}")
            print(f"Rating: {book_rating}")
            print(link_)




    

        

