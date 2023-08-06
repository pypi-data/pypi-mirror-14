from directory.exceptions import DirectoryException
from directory.models import Person

import requests
from lxml import html
from lxml.cssselect import CSSSelector

import re

# Base URL for the directory
directory_url = 'https://directory.middlebury.edu/'

search_url = 'https://directory.middlebury.edu/default.aspx'

person_url = 'https://directory.middlebury.edu/GetRecord.aspx'


def get_search_inputs():
    res = requests.get(directory_url)
    tree = html.fromstring(res.text)
    inputs = CSSSelector('#aspnetForm input, #aspnetForm select')
    return dict((i.get('name'), i.get('value', ''))
                for i in inputs(tree))


def get_results(search_fields):
    res = requests.post(search_url, data=search_fields)
    tree = html.fromstring(res.text)

    web_ids = [result.get('href').strip('#')
               for result in CSSSelector('.ResultItem .lnkName')(tree)]

    return [get_person(webid) for webid in web_ids]


def get_person(id):
    res = requests.get(person_url, params={'webid': id})
    tree = html.fromstring(res.text)

    attrs = dict(webid=id)
    for tr in CSSSelector('tr')(tree)[1:]:
        tds = tr.getchildren()
        key = (tds[0].text_content()
                     .strip().lower().replace(' ', '_').replace('-', ''))
        attrs[key] = tds[1].text_content().strip()

    return Person(**attrs)
