import multi_use_data_pulls as m
import hospital_dict as h
import functions as f


def get_files_for_multi_file_sources():
    """

    :return:
    """
    for item in h.hospital_dict:
        if len(item['filenames']) > 1:
            if len(item['facId']) > 1:
                m.multiple_file_pull(item['filenames'], item['url'])


def get_files_for_single_file_sources():
    """

    :return:
    """
    for item in h.hospital_dict:
        if len(item['filenames']) == 1:
            if len(item['facId']) > 1:
                m.single_file_pull(item['filenames'], item['url'])
