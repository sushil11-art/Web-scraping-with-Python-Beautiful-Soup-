import requests
from bs4 import BeautifulSoup
import csv
from lxml import html


outfile = open('books.csv', 'w', newline='')
writer = csv.writer(outfile)
writer.writerow(["BOOK TITLE", "BOOK PRICE",
                "STOCK AVAILABILITY", "More Info", "DESCRIPTION"])


def scrape_book_all():
    for i in range(1, 51):
        print(f"Loop count begin:{i}")
        # url = 'http://books.toscrape.com/catalogue/page-1.html'
        url = 'http://books.toscrape.com/catalogue/page-'+str(i)+'.html'
        text = requests.get(url).content
        soup = BeautifulSoup(text, 'lxml')
        books = soup.find_all(
            'li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        # print(books)
        for book in books:
            description_link = book.find(
                'article', class_="product_pod").h3.a["href"]
            book_title = book.find('article', class_="product_pod").h3.a.text
            price_stock = book.find('div', class_="product_price")
            book_price = price_stock.find(
                'p', class_="price_color").text
            stock_availability = price_stock.find(
                'p', class_="instock availability").text.replace(' ', '').strip()

            full_url = desc_full_url(description_link)

            response_text = requests.get(full_url)

            tree = html.fromstring(response_text.content)

            # print(tree)
            # response_text = requests.get(full_url).content
            # desc_soup = BeautifulSoup(response_text, 'lxml')
            # description_html = desc_soup.find(id="content_inner")
            try:
                desc_text = tree.xpath(
                    '//*[@id = "content_inner"]/article/p/text()')[0]
            except:
                desc_text = ""
            # if len(desc_text) > 0:
            #     text = desc_text[0]

            writer.writerow([book_title.strip(), book_price.strip(
            ), stock_availability.strip(), description_link.strip(), desc_text.strip()])
            # print(desc_text)
            # print(description_link)
            # print(book_price)
            # print(stock_availability)
    outfile.close()


def scrape_book_category():
    url = "http://books.toscrape.com"
    text = requests.get(url).content
    soup = BeautifulSoup(text, 'lxml')

    categories = soup.find('div', class_="side_categories").find(
        'ul', class_="nav nav-list").li.ul.find_all('li')
    # links = categories.find_all('a')["href"]
    url_categories = []
    for category in categories:
        link = category.find('a').get("href")
        full_url = 'http://books.toscrape.com/'+link
        url_categories.append(full_url)

    for cat in url_categories:
        reponse = requests.get(cat).content
        # reponse = requests.get(
        #     'http://books.toscrape.com/catalogue/category/books/crime_51/index.html').content
        bsoup = BeautifulSoup(reponse, 'lxml')
        category_name = bsoup.find(
            'div', class_="col-sm-8 col-md-9").find('div', class_="page-header action").h1.text
        print(category_name)
    print(url_categories)


def desc_full_url(description_link):
    url = 'http://books.toscrape.com/catalogue/'+str(description_link)
    return url


# http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html

# scrape_book_all()
scrape_book_category()

# //*[@id = "content_inner"]/article/p/text()
# //*[@id = "default"]/div/div/div/div/section/div[2]/div/ul/li[1]
