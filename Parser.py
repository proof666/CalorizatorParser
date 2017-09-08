import requests
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
r = requests.get(baseUrl + "product").text
soup = BeautifulSoup(r, "html.parser")
categoryHtmlList = soup.find_all('ul', {'class': 'product'})

for categoryHtml in categoryHtmlList:
    items = categoryHtml.find_all('li')
    for item in items:
        if item.find('a').get('href') == 'product/all':
            break

        productList = []
        name = item.find('a').text
        link = item.find('a').get('href')
        categoryRequest = requests.get(baseUrl + link).text
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
                nextPageRequest = requests.get(baseUrl + link + '?page=' + str(page)).text
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

print(categoryList)
