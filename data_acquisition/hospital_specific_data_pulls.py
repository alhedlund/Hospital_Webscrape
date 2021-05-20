"""
Some hospitals have several tabs or different formatting from the bulk of others.
These functions pull and output data specifically for them.
"""
import logging
import pandas as pd
from logging import DEBUG
import requests as r
import csv
from pprint import pprint as p
logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


def saint_alphonsus():
    """
    Pulls data for Saint Alphonsus hospitals and returns more workable output.
    :return:
    """
    types = ['oregon-idaho-shoppable.xlsx',
             'oregon-idaho-standard-charge.xlsx']
    results_array = []

    for item in types:
        url = 'https://www.trinity-health.org/assets/documents/price-transparency/'
        call_url = url + '{}'.format(item)
        data = r.get(call_url)
        with open(item, 'wb') as output:
            output.write(data.content)
            results_array.append(output)

    return results_array


def st_lukes(url: str, filename: str):
    """
     Pulls data for St. Luke's hospitals and returns more workable output.
    :param url:
    :param filename:
    :return:
    """
    data = r.get(url)
    with open(filename, 'wb') as output:
        output.write(data.content)
        # output.close()

    return data

