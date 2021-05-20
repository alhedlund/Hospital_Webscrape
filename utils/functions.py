import csv
import logging
import pandas as pd
from logging import DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


def clean_str(x):
    """
    Takes a string, removed special characters and returns a clean string.
    :param x: String
    :return: Clean string
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
    Takes the filename of an xlsx file and converts it to a csv file.
    :param filename: String representation of the filename.
    :return: csv version of xlsx file
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
    Takes the filename of a csv file and converts it into a dictionary object.
    :param filename: String representation of the filename.
    :return: Dictionary object
    """
    result = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            result.append(line)
    return result
