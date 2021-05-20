import logging
from logging import DEBUG
import requests as r
from pprint import pprint as p


logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


def multiple_file_pull(file_names: [str], url: str):
    """

    :param file_names:
    :param url:
    :return:
    """
    results_array = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    for item in file_names:
        call_url = url + '{}'.format(item)
        data = r.get(call_url, headers=headers)
        with open(item, 'wb') as output:
            output.write(data.content)
            results_array.append(output)
            print('Downloaded ' + item + ' ...')
    return results_array


def single_file_pull(file_name: [str], url: str):
    """

    :param file_name:
    :param url:
    :return:
    """
    call_url = url + '{}'.format(file_name[0])
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = r.get(call_url, headers=headers)
    with open(file_name[0], 'wb') as output:
        output.write(data.content)
        print('Downloaded ' + file_name[0] + ' ...')
    return output
