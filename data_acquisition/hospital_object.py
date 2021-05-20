import logging
import requests as r
import pandas as pd
from constants import hospital_dict as h
from logging import DEBUG
from pprint import pprint as p
from fuzzywuzzy import fuzz, process

logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


class Hospital:
    def __init___(self, fac_id, filenames, hospital_name, url):
        self.fac_id = fac_id
        self.filenames = filenames
        self.hospital_name = hospital_name
        self.url = url

    @staticmethod
    def get_hospital_fac_ids(self, hospital_dict, hospital_data):
        hospital_name = []
        similarity = []
        count = 0
        for i in hospital_dict['hospital']:
            ratio = process.extract(i, hospital_data['Facility Name'], limit=1)
            hospital_name.append(ratio[0][0])
            similarity.append(ratio[0][1])
            count += 1
            print(count)
        hospital_dict['hospital_name'] = pd.Series(hospital_name)
        hospital_dict['similarity'] = pd.Series(similarity)
        return pd.to_pickle(hospital_dict, 'hospital_matches')

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

    def get_files(self, filenames, fac_id, url):
        if len(filenames) == 1 and len(fac_id) > 1:
            self.single_file_pull(self, filenames, url)

        elif len(filenames) > 1 and len(fac_id) > 1:
            self.multiple_file_pull(self,filenames, url)

        else:
            return "There are no files form this hospital"
