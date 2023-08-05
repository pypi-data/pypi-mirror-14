import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import IptcEditor.src.data_reader as data_reader
from functools import partial
import subprocess


class Engine:
    # # # # WORKERS # # # #

    @staticmethod
    def replace_keywords(dataset=None,
                         old_keyword=None,
                         new_keyword=None):
        # # FILTERS & SET UP FILENAME/DIRECTORY
        if not dataset:
            return False
        filename = sanitize_filter(dataset[1]) if dataset[0] == 'F' else None
        # filter tag_to_replace
        old_keyword = sanitize_filter(old_keyword)
        # filter new tag
        new_keyword = sanitize_filter(new_keyword)
        # grab existing keyword list
        kwl = data_reader.DataReader.get_tags(new_keyword_list=[new_keyword],
                                              dataset=dataset,
                                              mode=data_reader.Mode.KEYWORDS)
        # filter tag_strings_list
        existing_keyword_list = list(
            map(sanitize_filter_taglist, kwl)) if kwl else None
        # # WORK
        if existing_keyword_list:
            for tag_list in existing_keyword_list:
                if tag_list:
                    # get filename associated with each tag_list
                    f = tag_list.pop()
                    # replace old string with new
                    if old_keyword:
                        for num, s in enumerate(tag_list):
                            if s == old_keyword:
                                if not new_keyword:
                                    # if no new tag, just delete the old
                                    del tag_list[num]
                                else:
                                    # replace the old tag with the new
                                    tag_list[num] = new_keyword
                    else:
                        # if a new tag (not a replacement), just add it
                        tag_list.append(new_keyword)
                    # delete the old strings (del_keywords method returns an obj that can be repr as str)
                    if 'returncode=1' in str(del_keywords(f)):
                        print('Keyword  not replaced - an error occurred!')
                    # add the new strings,
                    no_dupes = remove_dupes(tag_list)
                    if no_dupes:
                        # add the keywords. Note: "partial" allows passing of extra arg (f - the filename)
                        list(map(partial(add_keywords, f), no_dupes))
                else:
                    # if tag list is empty (i.e. there no existing tags)
                    add_keywords(filename, new_keyword)
        else:
            return False

    @staticmethod
    def remove_exif_field(dataset=None, dataset_to_remove=None):
        success = None
        if not dataset or not dataset_to_remove: return False
        if dataset[0] == 'F':
            for ds in dataset_to_remove:
                # run the del process, set success to True if at least 1 "non error" return
                success = True if del_dataset(
                    filename=sanitize_filter(dataset[1]), dataset=sanitize_filter(ds)) else print('Error')
        elif dataset[0] == 'D':
            directory = '{}/'.format(sanitize_filter(dataset[1]))  # get dir and add trailing slash
            file_list = [sanitize_filter(file) for file in os.listdir(directory) if os.path.isfile(
                '{}{}'.format(directory, file))]
            for f in file_list:
                for ds in dataset_to_remove:
                    filename = '{}{}'.format(directory, f)
                    success = True if del_dataset(
                        filename=filename, dataset=sanitize_filter(ds)) else print('Error')
        return success


# # # # HELPERS # # # #


def remove_dupes(sequence=None):
    if sequence:
        seen = set()
        seen_add = seen.add
        return [x for x in sequence if not (x in seen or seen_add(x))]
    return None


def sanitize_filter_taglist(tag_list=None):
    return list(map(sanitize_filter, tag_list)) if tag_list else None


def sanitize_filter(incoming=None):
    if not incoming: return None
    # sanitize the strings
    extra_chars = [':', '.', ' ', '|', '-', '~', '*', '/', '\[', '\]', '!', '_']
    return ''.join([c if c.isalnum() or c in extra_chars else '' for c in incoming])


# # SUBPROCESS (OS system / software calls) # #

def add_keywords(filename=None, tag=None):
    if not filename or not tag: return None
    filename = sanitize_filter(filename)
    tag = sanitize_filter(tag)
    subprocess.run(['exiv2', '-M', 'add Iptc.Application2.Keywords String {0}'.format(tag),
                    filename],
                   stdout=subprocess.PIPE, shell=False)
    return 'Tag {} added to {}.'.format(tag, filename)


def del_keywords(filename=None):
    if not filename: return None
    subprocess.run(['exiv2', '-M', 'del Iptc.Application2.Keywords', sanitize_filter(filename)],
                   stdout=subprocess.PIPE, shell=False)
    return True


def del_dataset(filename=None, dataset=None):
    if not filename or not dataset: return None
    result = subprocess.run(['exiv2', '-M', 'del {0}'.format(sanitize_filter(dataset)),
                             sanitize_filter(filename)],
                            stdout=subprocess.PIPE, shell=False)
    return True if 'returncode=0' in str(result) else False  # returncode=0 means no error from stdout
