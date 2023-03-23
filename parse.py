from selenium import webdriver
from bs4 import BeautifulSoup as bs


def parse():
    browser = webdriver.Chrome()
    browser.get("https://www.banki.ru/products/currency/cash/omsk/")
    source_data = browser.page_source
    soup = bs(source_data, features='html.parser')
    categories = soup.find('div', {'class':['table-flex__cell table-flex__cell--without-padding padding-left-default']})
    course = categories.text
    if ',' in course:
        course = course.replace(',', '.')
        course = float(course)
    print(course)

parse()