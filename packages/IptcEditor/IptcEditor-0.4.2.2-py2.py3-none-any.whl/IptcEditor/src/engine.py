#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import IptcEditor.src.data_reader as data_reader
from functools import partial
import subprocess
from lxml import etree


class Setup:
    CONFIG_DIR = '{}/.config/IptcEditor'.format(os.getenv('USERPROFILE') or os.getenv('HOME'))
    XML_FILENAME = 'tags.xml'
    FULL_XML_PATH = '{}/{}'.format(CONFIG_DIR, XML_FILENAME)


class XmlMachine:
    @staticmethod
    def create_new_xml_file():
        root = etree.Element("tags")
        root.set("version", "1.0")
        if not os.path.isfile(Setup.FULL_XML_PATH):
            tree_as_string = etree.tostring(element_or_tree=root,
                                            encoding="UTF-8",
                                            pretty_print=True,
                                            xml_declaration=True)
            with open(Setup.FULL_XML_PATH, "wb") as f:
                f.write(tree_as_string)
        return root

    @staticmethod
    def add_xml_tags(keywords=None):
        # tags is an incoming LIST of keywords
        if keywords:
            tree = XmlMachine.get_xml()
            if not tree:
                # create file if does not exist & try again
                XmlMachine.create_new_xml_file()
                XmlMachine.add_xml_tags(keywords=keywords)
            root = tree.getroot()
            existing_keywords_list = XmlMachine.get_keywords_from_xml(tree)
            for k in keywords:
                if k not in existing_keywords_list:  # only add kw if not already in the xml
                    tag_sub_element = etree.Element("tag", value=k)
                    root.append(tag_sub_element)
            # write back to file
            tree_as_string = etree.tostring(element_or_tree=root,
                                            encoding="UTF-8",
                                            pretty_print=True,
                                            xml_declaration=True)
            with open(Setup.FULL_XML_PATH, "wb") as f:
                f.write(tree_as_string)
            return root
        return None

    @staticmethod
    def get_xml():
        xml_file = Setup.FULL_XML_PATH
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.parse(xml_file, parser)
        except FileNotFoundError:
            return None

    @staticmethod
    def get_keywords_from_xml(xml=None):
        if not xml:
            xml = XmlMachine.get_xml()
        # returns list of keywords
        return [t.get("value") for t in xml.iterfind("tag")] if xml else None


class Engine:
    # # # # WORKERS # # # #

    @staticmethod
    def make_config_dir(path=None):
        if path:
            if not os.path.exists(path):
                os.mkdir(path)
                return True
        return None

    @staticmethod
    def replace_keywords(dataset=None,
                         keyword_to_replace=None,
                         new_keywords=None):
        # # FILTERS & SET UP FILENAME/DIRECTORY
        if not dataset:
            return False
        filename = sanitize_filter(dataset[1]) if dataset[0] == 'F' else None
        # filter tag_to_replace
        keyword_to_replace = sanitize_filter(keyword_to_replace)
        # filter new tag
        if new_keywords:
            new_keywords = [sanitize_filter(kw) for kw in new_keywords]
        # create new keyword list
        kwl = data_reader.DataReader.get_tags(new_keyword_list=new_keywords,
                                              dataset=dataset,
                                              mode=data_reader.Mode.KEYWORDS)
        # filter tag_strings_list
        existing_keyword_list = list(
            map(sanitize_filter_taglist, kwl)) if kwl else None
        # # WORK
        if existing_keyword_list:
            for kw_list in existing_keyword_list:
                if kw_list:
                    # get filename associated with each tag_list
                    f = kw_list.pop()
                    # replace old string with new
                    if keyword_to_replace:
                        for num, s in enumerate(kw_list):
                            if s == keyword_to_replace:
                                if not new_keywords:
                                    # if no new tag, just delete the old
                                    del kw_list[num]
                                else:
                                    # remove keyword-to-replace and add new list of keywords to the existing tag list
                                    del kw_list[num]
                                    kw_list += new_keywords
                    else:
                        # if a new tag (not a replacement), just add list of new keywords to existing
                        if new_keywords:
                            kw_list += new_keywords
                    # delete the old strings (del_keywords method returns an obj that can be repr as str)
                    if 'returncode=1' in str(del_keywords(f)):
                        print('Keyword  not replaced - an error occurred!')
                    # add the new strings,
                    no_dupes = remove_dupes(kw_list)
                    if no_dupes:
                        # add the keywords. Note: "partial" allows passing of extra arg (f - the filename)
                        list(map(partial(add_keywords, f), no_dupes))
                else:
                    # if tag list is empty (i.e. there no existing tags)
                    add_keywords(filename, remove_dupes(new_keywords))
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
        return [x for x in sequence if not (x in seen or seen.add(x))]
    return None


def sanitize_filter_taglist(tag_list=None):
    return list(map(sanitize_filter, tag_list)) if tag_list else None


def sanitize_filter(incoming=None):
    if not incoming: return None
    # sanitize the strings
    extra_chars = [':', '.', ' ', '|', '-', '~', '*', '/', '\[', '\]', '!', '_']
    return ''.join([c if c.isalnum() or c in extra_chars else '' for c in incoming])


# # SUBPROCESS (OS system / software calls) # #

def add_keywords(filename=None, new_keywords=None):
    # note, input NOT sanitised, as args already considered safe in called context.
    if not filename or not new_keywords: return None
    subprocess.run(['exiv2', '-M', 'add Iptc.Application2.Keywords String {0}'.format(new_keywords),
                    filename],
                   stdout=subprocess.PIPE, shell=False)
    # submit the new keywords to the xml machine, to add to xml kw archive if necessary
    XmlMachine.add_xml_tags(keywords=[new_keywords])
    return 'Keywords {} added to {}.'.format(new_keywords, filename)


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
