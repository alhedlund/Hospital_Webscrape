import logging
import requests as r
from logging import DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


class Hospital:
    def __init__(self, fac_id, filenames, hospital_name, url):
        self.fac_id = fac_id
        self.filenames = filenames
        self.hospital_name = hospital_name
        self.url = url

    @staticmethod
    def multiple_file_pull(self, file_names: [str], url: str):
        results_array = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
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

    @staticmethod
    def single_file_pull(self, file_name: [str], url: str):
        call_url = url + '{}'.format(file_name[0])
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = r.get(call_url, headers=headers)
        with open(file_name[0], 'wb') as output:
            output.write(data.content)
            print('Downloaded ' + file_name[0] + ' ...')
        return output

    def get_files(self):
        if len(self.filenames) == 1 and len(self.fac_id) > 1:
            self.single_file_pull(self, self.filenames, self.url)

        elif len(self.filenames) > 1 and len(self.fac_id) > 1:
            self.multiple_file_pull(self, self.filenames, self.url)

        else:
            return "There are no files from this hospital"
