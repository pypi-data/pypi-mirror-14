#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import subprocess
import magic

''' Definition Classes '''


class Mode:
    KEYWORDS = 'KEYWORDS'
    DATE = 'DATE'
    TAG_TYPES = 'TAG_TYPES'


class AcceptedFormats:
    FORMATS = ['image/jpg',
               'image/jpeg',
               'image/png',
               'image/tif',
               'image/tiff',
               'image/gif']


''' Worker Classes '''


class DataReader:
    @staticmethod
    def get_tags(new_keyword_list=None, dataset=None, mode=None):
        # set filename or directory
        if not dataset:
            return None
        filename = directory = None
        if dataset[0] == 'F':
            filename = sanitize_filter(dataset[1])
        elif dataset[0] == 'D':
            directory = '{}/'.format(sanitize_filter(dataset[1]))
        data_list = []
        # if handling single file, not a directory - and image extension is allowed ...
        if not directory and image_extension_checker(filename):
            if mode == Mode.KEYWORDS or mode == Mode.DATE:
                generated_data_list = Generators.generate_data_list(new_keyword_list, filename, mode)
                if generated_data_list:
                    data_list.append(generated_data_list)
                return data_list or False
            elif mode == Mode.TAG_TYPES:
                if Generators.generate_iptc_dataset_type_list(filename):
                    data_list.append(Generators.generate_iptc_dataset_type_list(filename)) or False
                return data_list or False
        elif directory:
            # if handling a directory ...
            file_list = [sanitize_filter(file) for file in os.listdir(directory)
                         if os.path.isfile('{}{}'.format(directory, file))]
            if mode == Mode.KEYWORDS or mode == Mode.DATE:
                for f in file_list:
                    f = '{}{}'.format(directory, f)
                    # generate tag list, but only if image extension checker passes
                    more_tags = Generators.generate_data_list(new_keyword_list, f, mode) \
                        if image_extension_checker(f) else None
                    if more_tags:
                        # append a new list inside the tagStringsContainer list containing the file tags
                        data_list.append([tag for tag in more_tags])
                        # delete the temp holding list values, ready for re-use
                        del more_tags[:]
                return data_list or False
            elif mode == Mode.TAG_TYPES:
                for f in file_list:
                    f = '{}{}'.format(directory, f)
                    more_tags = Generators.generate_iptc_dataset_type_list(filename=f) \
                        if image_extension_checker(f) else None
                    if more_tags:
                        data_list.append([tag for tag in more_tags])
                        del more_tags[:]
                return data_list or False
        else:
            return False


class Generators:
    @staticmethod
    def generate_data_list(new_keywords_list=None, filename=None, mode=None):
        tag_strings = []
        filename = sanitize_filter(filename) if filename else None
        # examine the existing IPTC tags
        try:
            examine = subprocess.Popen(['exiv2', '-PI', filename], stdout=subprocess.PIPE, shell=False)
            output, error = examine.communicate()
        except FileNotFoundError:
            return False
        if output:
            # decode the binary output to string
            decoded_output = output.decode()
            # split the string at linebreak, into a list of discrete tags
            tag_list = decoded_output.split('\n')
            # create a list in which to place each element of every tag
            elements_list = []
            ''' loop the tag list and add - to the new elements_list list - NEW lists of tags, split into elements,
            created by splitting the tag string at whitespace (default split())
            elements_list will be a list of lists of elements.
            '''
            for tag in tag_list:
                elements_list.append(tag.split())
            # loop the elements_list (which is a list of lists of elements)
            string_builder_keywords = []
            string_builder_date = []
            for listOfElements in elements_list:
                if listOfElements and listOfElements[0] == 'Iptc.Application2.Keywords':
                    # append small lists of each element number 3 and above, to the new string_builder list
                    string_builder_keywords.append(listOfElements[3:])
                elif listOfElements and listOfElements[0] == 'Iptc.Application2.DateCreated':
                    string_builder_date.append(listOfElements[3:])
            ''' add each complete tag string (elements of string_builder_ joined to string)
            as an element in the new tagStrings list
            '''
            if mode == Mode.KEYWORDS:
                for element in string_builder_keywords:
                    tag_strings.append(' '.join(element))
                # append the filename to the new list of file tags
                if tag_strings:
                    tag_strings.append(filename)
                return tag_strings
            elif mode == Mode.DATE:
                for element in string_builder_date:
                    tag_strings.append(' '.join(element))
                if tag_strings:
                    tag_strings.append(filename)
                return tag_strings
        elif not output and new_keywords_list:
            # if no existing list, but entirely new list has been set (for when method called when adding tags)
            for i in new_keywords_list:
                # add items from list of new keywords (only 1 now, unless updated to accept additional (delimited)
                tag_strings.append(sanitize_filter(i))
            tag_strings.append(filename)
            # return the new list
            return tag_strings
        else:
            return False

    @staticmethod
    def generate_iptc_dataset_type_list(filename=None):
        tag_types = []
        filename = sanitize_filter(filename) if filename else None
        # examine the existing IPTC tags types
        try:
            examine = subprocess.Popen(['exiv2', '-PI', filename], stdout=subprocess.PIPE, shell=False)
            output, error = examine.communicate()
        except FileNotFoundError:
            return False
        if output:
            # decode the binary output to string
            decoded_output = output.decode()
            # split the string at linebreak, into a list of discrete tags
            tag_list = decoded_output.split('\n')
            # create a list in which to place each element of every tag
            elements_list = []
            for tag in tag_list:
                elements_list.append(tag.split())
            # loop the elements_list (which is a list of lists of elements)
            for listOfElements in elements_list:
                if listOfElements:
                    tag_types.append(listOfElements[0])
            tag_types.append(filename)
            return remove_dupes(tag_types)
        else:
            # if no tags
            return False


''' HELPERS '''


def image_extension_checker(filename=None):
    # # set up magic method (from imported 'magic' package) to test mime type
    filename = sanitize_filter(filename) if filename else None
    mime_check = magic.open(magic.MAGIC_MIME_TYPE)
    mime_check.load()
    return True if filename and \
                   mime_check.file(filename) in AcceptedFormats.FORMATS else False


def remove_dupes(tag_list=None):
    discrete = set()
    no_dupes = []
    if tag_list:
        for tag in tag_list:
            if tag not in discrete:
                no_dupes.append(sanitize_filter(tag))
            discrete.add(sanitize_filter(tag))
    return no_dupes


def sanitize_filter(incoming=None):
    if not incoming: return None
    # sanitize the strings
    extra_chars = [':', '.', ' ', '|', '-', '~', '*', '/', '\[', '\]', '!', '_']
    return ''.join([c if c.isalnum() or c in extra_chars else '' for c in incoming])
