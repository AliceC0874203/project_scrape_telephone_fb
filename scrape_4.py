#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'jolopots'

import requests
import json
import csv
from bs4 import BeautifulSoup


class LazadaProducts:
    def __init__(self, prod_input):
        self.main_link = 'https://www.lazada.com.ph/catalog/?{}'
        self.to_search = '&q={}'.format(prod_input)
        self.prod_input = prod_input
        self.csv_fname = 'lazada_products_{}.csv'.format(prod_input)

    def write_csv(self, prod_results):
        with open(self.csv_fname, 'a', newline='') as f:
            writer = csv.writer(f)

            for prod in prod_results:
                writer.writerow(prod)

    def get_products(self):
        r = requests.get(self.main_link.format(self.to_search))
        soup = BeautifulSoup(r.text, 'lxml')

        products = soup.find('script', type='application/ld+json').find_next_sibling().get_text()
        data = json.loads(products)
        prod_results = [(elem.get('name'), 'PHP' + elem.get('offers').get('price')) for elem in
                        data.get('itemListElement')]

        self.write_csv(prod_results)

        while True:
            pagination = soup.find('link', rel="next")
            if not pagination:
                break
            else:
                new_query = (pagination.get('href') + '{}').format(self.to_search)
                r = requests.get(new_query)
                soup = BeautifulSoup(r.text, 'lxml')

                products = soup.find('script', type='application/ld+json').find_next_sibling().get_text()
                data = json.loads(products)
                prod_results = [(elem.get('name'), 'PHP' + elem.get('offers').get('price')) for elem in
                                data.get('itemListElement')]

                self.write_csv(prod_results)


if __name__ == '__main__':
    prod_input = input('What product? ')

    laz = LazadaProducts(prod_input)
    laz.get_products()