#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import codecs
from bs4 import BeautifulSoup
	

def parse_product(product_html):
    single_product = dict()
    single_product['name'] = product_html.find('td', {'class': 'views-field-title'}).find('a').text.strip()
    single_product['protein'] = product_html.find('td', {'class': 'views-field-field-protein-value'}).text.strip()
    single_product['fat'] = product_html.find('td', {'class': 'views-field-field-fat-value'}).text.strip()
    single_product['carbohydrate'] = product_html.find('td', {'class': 'views-field-field-carbohydrate-value'}).text.strip()
    single_product['kcal'] = product_html.find('td', {'class': 'views-field-field-kcal-value'}).text.strip()
    return single_product
 
baseUrl = "http://www.calorizator.ru/"
categoryList = dict()

proxies = {
  'http': 'hqproxyusr1.avp.ru:8080',
  'https': 'hqproxyusr1.avp.ru:8080',
}
r = requests.get(baseUrl + "product",proxies=proxies).text
soup = BeautifulSoup(r, "html.parser")
categoryHtmlList = soup.find_all('ul', {'class': 'product'})

print('Parsing data for you, please be patient and drink some tea')

ct = 0
for categoryHtml in categoryHtmlList:
    items = categoryHtml.find_all('li')
    if ct > 1:
        break
    ct += 1
    for item in items:
        if item.find('a').get('href') == 'product/all':
            break
        if ct > 2:
            break
        ct += 1
        print(ct)
        productList = []
        name = item.find('a').text
        link = item.find('a').get('href')
        categoryRequest = requests.get(baseUrl + link,proxies=proxies).text
        categorySoup = BeautifulSoup(categoryRequest, "html.parser")
        pagerHtml = categorySoup.find('ul', {'class': 'pager'})

        productsHtmlList = categorySoup \
            .find('table', {'class': 'views-table'}) \
            .find('tbody') \
            .find_all('tr')

        for productHtml in productsHtmlList:
            product = parse_product(productHtml)
            productList.append(product)

        if pagerHtml is not None:
            pagesHtml = pagerHtml.find_all('li', {'class': 'pager-item'})
            page = 1
            while page <= len(pagesHtml):
                nextPageRequest = requests.get(baseUrl + link + '?page=' + str(page),proxies=proxies).text
                categorySoup = BeautifulSoup(nextPageRequest, "html.parser")
                page += 1

                productsHtmlList = categorySoup \
                    .find('table', {'class': 'views-table'}) \
                    .find('tbody') \
                    .find_all('tr')

                for productHtml in productsHtmlList:
                    product = parse_product(productHtml)
                    productList.append(product)

        categoryList[name] = productList

with codecs.open('products.json', 'w', encoding='utf-8') as file:
    json.dump(categoryList, file, ensure_ascii=False)

print('Ready!!!')
