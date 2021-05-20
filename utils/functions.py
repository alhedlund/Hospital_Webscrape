import logging
import pandas as pd
from logging import DEBUG
import requests as r
import csv
from pprint import pprint as p
import numpy as np
from utils import DataFrameTools as dft
from constants import hospital_dict as h
from fuzzywuzzy import fuzz, process


def clean_str(x):
    """

    :param x:
    :return:
    """
    x2 = x.lower()
    x2 = x2.replace('.', ''). \
        replace("'", ''). \
        replace('-', ''). \
        replace('(', ''). \
        replace(')', ''). \
        replace('&', ''). \
        replace('/', '')
    return x2


def convert_xlsx_to_csv(filename):
    """

    :param filename:
    :return:
    """
    df = pd.DataFrame()
    read_file = pd.ExcelFile(filename, engine='openpyxl')
    for sheet in read_file.sheet_names:
        df_tmp = read_file.parse(sheet)
        df = df.append(df_tmp, ignore_index=True, sort=False)
    csv_file = df.to_csv(filename[0:-5]+'.csv', index=False, header=True)
    return csv_file


def csv_to_dict(filename):
    """

    :param filename:
    :return:
    """
    result = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            result.append(line)
    return result


def get_hospital_fac_ids(hospital_dict, hospital_data):
    """

    :param hospital_dict:
    :param hospital_data:
    :return:
    """
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

