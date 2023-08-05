=================
**Description**
=================


Please note, this is a very early beta ...

This is a python3 GTK3 wrapper for the EXIV2 application, used to read and edit IPTC image metadata.
This application can handle bulk operations on directories of image files.
Currently the application only allows *editing* of IPTC keywords (Iptc.Application2.Keyword).
However, all IPTC datasets may be *displayed* or *removed*.

============
**Features**
============

- Read and edit IPTC image metadata.
- Select to operate on a single image file, or do bulk operations on a directory of image files.
- Allows for complete removal of unrequired IPTC datasets.

===========
**Usage**
===========

- Either select a single image file, or a directory containing image files.
  Acceptable mime image types are: jpg, jpeg, tif, tiff, png, gif.
- Switch to the Tagger tab to work on your selection.
- These functions are available:

  - Display Keywords (button): Shows all the keywords of the selected file(s).
  - Display Date Created (button): Shows all the "DateCreated" tags of the selected file(s).
  - Display IPTC Datasets (button): Shows all the IPTC tag types of the selected file(s).
  - Replace existing keyword:

    - Type the keyword you wish to replace in the "keyword to replace" field.
      Be sure to type it *exactly* as it is. This is cAse sEnsItiVe.
    - Type the new keyword into the "New key phrase" field.
    - Tap the "Replace keyword(s) button.

  - Add a new keyword:

    - Do as above (replacement), but leave the "keyword to replace" field empty.

  - Delete an existing keyword:

    - Do as above (replacement), but leave the "New keyword" field empty.

  - Remove IPTC dataset:

    - Type IPTC dataset identifier *exactly as it appears* into the "Remove IPTC Dataset" field.
    - Tap the "Remove IPTC Dataset" button.

=============
**Version**
=============

For the current version number, see IptcEditor/VERSION.rst

=============
**Roadmap**
=============

- Add ability to *view*, *add* and *edit* additional IPTC datasets
- Add support for additional types of metadata

