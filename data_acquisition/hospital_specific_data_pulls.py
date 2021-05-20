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

    :param url:
    :param filename:
    :return:
    """
    data = r.get(url)
    with open(filename, 'wb') as output:
        output.write(data.content)
        # output.close()

    return data

