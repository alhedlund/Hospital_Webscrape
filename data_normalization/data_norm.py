import pandas as pd
import logging
from sqlalchemy import create_engine
from utils import functions
from utils import sql
from constants import hospital_dict as h
from data_acquisition import hospital_object as hosp_obj
from logging import DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(level=DEBUG)


def recursive_col_elimination(dataframe, filename, k=0):
    """
    Takes a dataframe and recursively trims rows until columns of interest are at 0th index.
    :param dataframe: raw dataframe from read file
    :param filename: name of file being read
    :param k:
    :return new_df: dataframe with columns of interest at the 0th index
    """
    dataframe = dataframe[dataframe.columns.drop(list(dataframe.filter(regex='.*Unnamed.*')))]

    col_len = len(dataframe.columns)

    if col_len <= 1:
        new_dataframe = pd.read_csv(filepath_or_buffer=filename, header=k+1, dtype=str, engine='python')
        dataframe = recursive_col_elimination(new_dataframe, filename, k=k+1)

    return dataframe


def write_raw_csv_to_table(dataframe: pd.DataFrame, fac_id: str, hospital_name: str, year: str):
    """
    Takes a dataframe and writes contents to a table with the specified name.
    This should be executed after columns are cleaned up in recursive_col_elimination function.
    :param dataframe: Dataframe with correct columns
    :param fac_id: String containing facility_id field
    :param hospital_name: String containing hospital_name field
    :param year: Year file is relevant to
    """
    column_names = []
    table_name = str(fac_id) + '_' + str(hospital_name).replace(' ', '_') + '_' + year
    for item in dataframe.columns:
        item = item.replace(" ", "_")
        column_names.append(item + ' VARCHAR(255)')
    column_names = str(column_names).replace("'", '')[1:-1]
    create_table_sql = '''
                        CREATE TABLE {} (
                        {}
                        )
                        '''.format(table_name, column_names)

    engine = create_engine(
        'mysql+pymysql://admin:Clearwater123!@MySQL-database-1.cmx12ym6czg5.us-west-2.rds.amazonaws.com/dbo')

    sql.sql_commit(create_table_sql)
    dataframe.to_sql(name=table_name, con=engine, if_exists='replace')


def basic_norm_function(dataframe):
    """
    Takes a dataframe with correct columns and extracts common columns of interest via regex, returning a
    normed dataframe.
    :param dataframe: dataframe with columns of interest at 0th index
    :return normed_df: dataframe with only common columns
    """
    normed_col_list = ['.*HCPCS.*', '.*CPT.*', '.*Code.*', '.*Description.*', '.*Charge.*', '.*Price.*', '.*Cost.*']
    new_cols = []

    for col_name in normed_col_list:
        df_subset_contains = dataframe.filter(regex=col_name, axis=1)
        new_cols.append(list(df_subset_contains.columns))

    normed_df = dataframe[set(column for i in new_cols for column in i)]

    normed_df = normed_df.dropna()

    return normed_df


##########################################
# runs functions for example
# csv test: 100242
# xlsx test: 50512

# Testing the class
for i in h.hospital_dict:
    hosp_one = hosp_obj.Hospital(i['facId'], i['filenames'], i['hospital'], i['url'])
    hosp_one.get_files()

    for file in hosp_one.filenames:
        if file[-5:].count('.xlsx') >= 1:
            csv_file, csv_filename = functions.convert_xlsx_to_csv(file)

            df = pd.read_csv(filepath_or_buffer=csv_filename)
            cor_df = recursive_col_elimination(dataframe=df, filename=csv_filename)

            print(df.columns)
            print(cor_df.columns)

            normed_dataframe = basic_norm_function(cor_df)
            # write_raw_csv_to_table(normed_dataframe, hosp_one.fac_id, hosp_one.hospital_name, '2020')

        elif file[-4:].count('.csv') >= 1:
            df = pd.read_csv(filepath_or_buffer=file, engine='python')
            cor_df = recursive_col_elimination(dataframe=df, filename=file)

            print(df.columns)
            print(cor_df.columns)

            normed_dataframe = basic_norm_function(cor_df)
            print(normed_dataframe)
            write_raw_csv_to_table(normed_dataframe, hosp_one.fac_id, hosp_one.hospital_name, '2020')
        quit()

