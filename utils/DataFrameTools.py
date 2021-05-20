import logging
from ast import literal_eval
from json import loads
from os import path, stat, mkdir, startfile
from webbrowser import open_new_tab
from pandas import DataFrame, Series, read_csv, ExcelWriter
from utils import log

logger = logging.getLogger(log.LOGGER_NAME)


def importDataFrameFromCSV(filepath):
    try:
        saved_df: DataFrame = read_csv(filepath)
        return saved_df
    except AssertionError as error:
        print(error)


def compairDataFrames(existing_df: DataFrame, new_df: DataFrame, identifier='identifier'):
    existing_data_identifiers = getColumnDataFromDataFrame(existing_df, identifier)
    new_data_identifiers = getColumnDataFromDataFrame(new_df, identifier)
    for id in new_data_identifiers:
        if id not in existing_data_identifiers:
            print('Adding new issue: '+str(id))
            existing_df = existing_df.append(new_df.loc[new_df['identifier'] == id], sort= False)
        else:
            print('Ignoring Duplicated error: '+id)

    return existing_df


def dataFrameToFile(df: DataFrame, filename: str, action='overwrite',
                    directory='output_df_to_file\\'):
    file_path = directory + filename
    try:
        stat(directory)
    except FileNotFoundError as error:
        mkdir(directory)

    if action == 'merge':
        try:
            if path.isfile(file_path):
                savedDF: DataFrame = read_csv(file_path)
                consolidated_df: DataFrame = compairDataFrames(existing_df=savedDF, new_df=df)
                doc = consolidated_df.to_csv(index=False)
                file = open(file_path, 'w')
                file.write(doc)
                file.close()
            else:
                doc = df.to_csv(index=False)
                file = open(file_path, 'w')
                file.write(doc)
                file.close()
                print('DataFrame to CSV export successful, fileName: '+ file_path)
        except AssertionError as error:
            print('Error in dataFrameToFile, see exception below:')
            print(error)
    elif action == 'overwrite':
        try:
            doc: str = df.to_csv(index=False)
            doc = doc.replace('\r', '')
            file = open(file_path, 'w')
            file.write(doc)
            file.close()
            print('DataFrame to CSV export successful, fileName: '+ file_path)
        except AssertionError as error:
            print('Error in dataFrameToFile, see exception below:')
            print(error)
    else:
        print('no action taken in dataFrameToFile due to action conditional...')


# Data Access Functions

def getColumnDataFromDataFrame(df: DataFrame, columnHeader: str):
    temp_list: list = []
    for data in df[columnHeader]:
        try:
            temp_list.append(data)
        except:
            continue
    return temp_list


def getRowsFromDataFrameForIdentifiers(df: DataFrame, identifier_list: list, column_header):
    df_identifiers = getColumnDataFromDataFrame(df, column_header)
    results: DataFrame = DataFrame()
    for id in identifier_list:
        if id in df_identifiers:
            results: DataFrame = results.append(df.loc[df[column_header] == id], sort=False)
    return results


def parseJsonfromSeries(series: Series):
    json_list = []
    for row in series:
        json_list.append(loads(row))
    return json_list


# Data Export Functions

HTML = '''<html>
        <header>
        <style>
            table, th, td { border-collapse:collapse;
            
            
            
            }
            th { text-align: center;
            padding: 1px;
            }
            td {
            white-space: nowrap;
            overflow: auto;
            padding: 0px;
            text-align: center;
            border-top: 1px solid #d3e4ff;
            }
        </style>
        </header>
    <body>
    <h4></h4>'''

HTML_middle = '''
            <h4></h4>'''

HTML_end = '''  </body>

</html>'''


def dictionartyToHTMLOpen(dictionary: dict, filename: str = 'test_from_dict'):
    dataFrameToHTMLFileWriteAndOpen(DataFrame(dictionary), filename)


def dataFrameToHTMLFileWriteAndOpen(df: DataFrame, filename: str = 'test', directory: str = 'html_output\\'):
    file_extension = '.html'
    file_path = filename + file_extension
    if directory != '':
        try:
            stat(directory)
            file_path = directory + filename + file_extension
        except:
            mkdir(directory)
            file_path = directory + filename + file_extension
    try:
        doc = HTML + df.to_html() + HTML_end
        file = open(file_path, 'w')
        file.write(doc)
        file.close()
        open_new_tab(file_path)
        logger.info('DataFrame to HTML export successful, filename: ' + filename)
    except AssertionError as error:
        logger.error(
            'Error in dataFrameToHTMLFile, see exception below:\n' + str(error))


def hTMLFileWriteAndOpen(html, filename: str, open_opt=True):
    try:
        doc = html
        file = open(filename + '.html', 'w')
        file.write(doc)
        file.close()
        if open_opt:
            open_new_tab(filename + '.html')
        print('DataFrame to HTML export successful, filename: ' + filename)
    except AssertionError as error:
        print('Error in dataFrameToHTMLFile, see exception below:')
        print(error)


def write_styled_data_frame(styled_df: DataFrame.style, filename, extension, directory='', open_opt=False):
    file_path = filename + extension
    if directory != '':
        try:
            stat(directory)
            file_path = directory + filename + extension
        except:
            mkdir(directory)
            file_path = directory + filename + extension
    try:
        if extension == '.xlsx':
            filename = directory + filename + extension
            writer = ExcelWriter(filename, engine='xlsxwriter')
            styled_df.to_excel(writer, sheet_name='results')
            writer.save()
            logger.info('xlsx output successful: ' + filename)
        elif extension == '.html':
            doc = styled_df.render()
            filename = directory + filename + extension
            file = open(filename, 'w')
            file.write(doc)
            file.close()
            logger.info('html output successful: ' + filename)
        if open_opt:
            startfile(filepath=file_path)
    except BlockingIOError as error:
        logger.error(
            'error in write_styled_data_frame see exception:\n' + str(error))


# Formatting DataFrames

def applyBackground(row: list, location: int, ifTrueColor = 'white', ifFalseColor = '#f9bbbb'):
    if row[location] is False:
        return Series('background-color: ' + ifFalseColor, row.index)
    else:
        return Series('background-color: ' + ifTrueColor, row.index)


def highlight_vals(value: int, trueColor = 'green', falseColor = 'red'):
    if value >= 95:
        return 'color: %s' % trueColor
    else:
        return 'color: %s' % falseColor


def bold_values(value):
    return 'font-weight: %s' % 'bold'


def bold_team_row(row):
    if 'team' in str.lower(row[0]):
        return Series('font-weight: %s' % 'bold', row.index)
    else:
        return Series('font-weight: %s' % 'normal', row.index)


def apply_background(row):
    if 'team' in str.lower(row[0]):
        return Series('background-color: #d3e4ff', row.index)
    else:
        return Series('background-color: white', row.index)


def summaryBold(row):
    if 'overall' in str.lower(row[0]):
        return Series('background-color: #d3e4ff', row.index)
    else:
        return Series('background-color: white', row.index)


# Data Manipulation Functions


def aliasDataFrameHeaders(df: DataFrame, alias: str):
    origVals: list = list(df.coilumns.values)
    text = '{'
    for val in origVals:
        indx = origVals.index(val)
        if indx > 0: text = text + ', '
        text = text + '\"' + val + '\"' + '\"' + alias + '.' + val + '\"'
        if indx == (origVals.__len__()-1): text = text + '}'
    '''
    https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
    literal_eval(node_or_string)
    Safely evaluate an expression or node or a string containing a Python
    expression. The string or note provided may only consist of the following Python
    literal structures: strings, numbers, tuples, lists, dicts, booleans, and None.
    '''
    text: dict = literal_eval(text)
    df.rename(columns=text, inplace=True)
    print(text)
    return df


