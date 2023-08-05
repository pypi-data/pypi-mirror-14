# -*- coding: utf-8 -*-

import re
from xml.dom import minidom


class DataParser(object):

    def __init__(self, input_file):
        self.input_file = input_file
        self.products = []

    # TODO: Компановка сервсиных контрактов
    # 36 мес. нужно предстваить как три контракта по 12 мес.
    # TODO: Проверка загруженного файла на соответствие XML схеме
    def parse(self):
        xmldoc = minidom.parse(self.input_file)
        product_item_list = xmldoc.getElementsByTagName('ProductLineItem')
        parent_product_index = None
        for product_item in product_item_list:
            product_line_number = product_item.getElementsByTagName('LineNumber')[0].firstChild.data
            product_name = product_item.getElementsByTagName('ProductIdentifier')[0].firstChild.data
            product_description = product_item.getElementsByTagName('Description')[0].firstChild.data
            product_count = product_item.getElementsByTagName('Quantity')[0].firstChild.data
            product_price = product_item.getElementsByTagName('UnitListPrice')[0].firstChild.data
            service_duration = None

            # noinspection PyPep8
            if re.search('.+?=', product_name):
                product_type = 'spare'
            elif product_item.getElementsByTagName('itemType') and re.search("SERVICE",
                                                                             product_item.getElementsByTagName(
                                                                                        'ProductType')[0].firstChild.data):
                product_type = 'service'
                service_duration = product_item.getElementsByTagName('Duration')[0].firstChild.data
            else:
                product_type = 'other'

            if int(product_line_number.split('.')[-1]) == 0:
                self.products.append({
                    'number': product_line_number,
                    'name': product_name,
                    'description': product_description,
                    'count': product_count,
                    'price': product_price,
                    'type': product_type,
                    'components': [],
                    'services': []
                })
                parent_product_index = len(self.products) - 1
            else:
                if product_type != 'service':
                    component = {
                        'number': product_line_number,
                        'name': product_name,
                        'description': product_description,
                        'count': product_count,
                        'price': product_price
                    }
                    self.products[parent_product_index]['components'].append(component)
                else:
                    service = {
                        'number': product_line_number,
                        'name': product_name,
                        'description': product_description,
                        'duration': service_duration,
                        'count': product_count,
                        'price': product_price
                    }
                    self.products[parent_product_index]['services'].append(service)
