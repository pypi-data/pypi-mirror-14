# -*- coding: utf-8 -*-
import urllib
from xml.dom import minidom

# TODO: Дописать проверку на успешное выоплнение запроса к cbr.ru

class ExchangeRate(object):
    url_string = "http://www.cbr.ru/scripts/XML_daily.asp"
    rates = {}

    def __init__(self):
        url = urllib.urlopen(self.url_string)
        self.data = url.read()
        self.data.decode('windows-1251')

        xmldoc = minidom.parseString(self.data)
        rates_values = xmldoc.getElementsByTagName("Valute")
        for rate in rates_values:
            name = rate.getElementsByTagName("Name")[0].firstChild.nodeValue
            char_code = rate.getElementsByTagName(
                "CharCode")[0].firstChild.nodeValue
            nominal = rate.getElementsByTagName(
                "Nominal")[0].firstChild.nodeValue
            value = rate.getElementsByTagName("Value")[0].firstChild.nodeValue

            self.rates[char_code] = {
                'name': name,
                'nominal': nominal,
                'value': value
            }

    # TODO: Нужно более лаконично описать return в формате float
    def get_value(self, char_code):
        if self.rates and self.rates[char_code]:
            return str("%.2f" % float(self.rates[char_code]['value'].replace(',', '.'))).replace('.', ',')
        else:
            return ""
