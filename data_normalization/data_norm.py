import pandas as pd
from sqlalchemy import create_engine
from hospital_dict import hospital_dict
from multi_use_data_pulls import single_file_pull, multiple_file_pull
from functions import convert_xlsx_to_csv
import sql
import DataFrameTools as dft
hospital_data = []


def get_files_from_fac_id(facility_id: str):
    global hospital_data
    """
    Takes a facility id string and executes function to pull files from website
    :param facility_id:
    :return:
    """
    for i in hospital_dict:
        if i['facId'] == facility_id:
            filenames = i['filenames']
            url = i['url']
            if filenames[0][-4:] == '.csv':
                if len(filenames) > 1:
                    multiple_file_pull(file_names=filenames, url=url)
                else:
                    single_file_pull(file_name=filenames, url=url)
                hospital_data.append(i['facId'])
                hospital_data.append(i['hospital'])
                return filenames


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


def write_raw_csv_to_table(dataframe: pd.DataFrame, hospital, year: str):
    global hospital_data
    """
    Takes a dataframe and writes contents to a table with the specified name.
    This should be executed after columns are cleaned up in recursive_col_elimination function.
    :param dataframe: dataframe with correct columns
    :param hospital: Name of mysql table data will go in to
    """
    column_names = []
    table_name = str(hospital[0]) + '_' + str(hospital[1]).replace(' ', '_') + '_' + year
    for item in dataframe.columns:
        item = item.replace(" ", "_")
        column_names.append(item + ' VARCHAR(255)')
    column_names = str(column_names).replace("'", '')[1:-1]
    create_table_sql = '''
                        CREATE TABLE {} (
                        {}
                        )
                        '''.format(table_name, column_names)
    print(create_table_sql)
    print(table_name)

    engine = create_engine(
        'mysql+pymysql://admin:Clearwater123!@MySQL-database-1.cmx12ym6czg5.us-west-2.rds.amazonaws.com/dbo')

    # Todo: Add programmatic table creation here as well
    sql.sql_commit(create_table_sql)
    dataframe.to_sql(name=table_name, con=engine, if_exists='replace')
    hospital_data.clear()
    print(hospital_data)


def basic_norm_function(dataframe):
    """
    Takes a dataframe with correct columns and extracts common columns of interest via regex, returning a
    normed dataframe.
    :param dataframe: dataframe with columns of interest at 0th index
    :param filename: name of file being read
    :return normed_df: dataframe with only common columns
    """
    # Todo: Decide columns we want to keep across all files to formalize this list of terms
    normed_col_list = ['.*HCPCS.*', '.*CPT.*', '.*Code.*', '.*Description.*', '.*Charge.*', '.*Price.*', '.*Cost.*']
    new_cols = []

    for i in normed_col_list:
        df_subset_contains = dataframe.filter(regex=i, axis=1)
        new_cols.append(list(df_subset_contains.columns))

    normed_df = dataframe[set(column for i in new_cols for column in i)]

    normed_df = normed_df.dropna()

    return normed_df


##########################################
# runs functions for example
# csv test: 100242
# xlsx test: 50512
fac_id_filenames = get_files_from_fac_id('131312')

print(fac_id_filenames)
for filename in fac_id_filenames:
    print(filename)

    if filename.count('.xlsx') >= 1:
        csv_file, csv_filename = convert_xlsx_to_csv(filename)

        df = pd.read_csv(filepath_or_buffer=csv_filename)
        cor_df = recursive_col_elimination(dataframe=df, filename=csv_filename)

        print(df.columns)
        print(cor_df.columns)

        normed_dataframe = basic_norm_function(cor_df)
        write_raw_csv_to_table(normed_dataframe, hospital_data, '2020')

    elif filename.count('.csv') >= 1:
        df = pd.read_csv(filepath_or_buffer=filename, engine='python')
        cor_df = recursive_col_elimination(dataframe=df, filename=filename)

        print(df.columns)
        print(cor_df.columns)

        normed_dataframe = basic_norm_function(cor_df)
        write_raw_csv_to_table(normed_dataframe, hospital_data, '2020')
