# ~*~ coding: utf-8 ~*~
import os
import urllib2
import datetime

from lxml import etree
from django.conf import settings

from virtenviro.shop.models import Currency


def update_currency():
    current_date = datetime.datetime.now()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s' % (current_date.day,
                                                                         current_date.month, current_date.year)
    xml_file = os.path.join(settings.MEDIA_ROOT, 'Valute%s.%s.%s.xml' % (current_date.day,
                                                                         current_date.month, current_date.year))
    f = open(xml_file, 'wb')
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
    response = opener.open(url)
    data = response.read()
    opener.close()
    f.write(data)
    f.close()
    '''
    Fields in xml
    Valute
        NumCode
        CharCode
        Nominal
        Name
        Value
    '''
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_file, parser)
    for valute in tree.iterfind('.//Valute'):
        name = valute.find('Name').text
        try:
            currency = Currency.objects.get(name=name)
        except Currency.DoesNotExist:
            continue
        currency.char_code = valute.find('CharCode').text
        currency.num_code = int(valute.find('NumCode').text)
        currency.value = float(valute.find('Value').text)
        currency.nominal = float(valute.find('Nominal').text)
        currency.save()

