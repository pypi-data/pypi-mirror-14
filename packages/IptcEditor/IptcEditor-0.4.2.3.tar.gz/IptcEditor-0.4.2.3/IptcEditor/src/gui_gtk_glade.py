#!/usr/bin/env python3
import os
import gi
import magic
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import IptcEditor.src.engine as engine
import IptcEditor.src.data_reader as data_reader

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class GuiGtkGlade:

    def __init__(self):

        # project_root = os.path.dirname(os.path.realpath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(__file__))

        # make the config directory if does not exist
        user_home = os.getenv('USERPROFILE') or os.getenv('HOME')
        engine.Engine.make_config_dir(path='{}/.config/IptcEditor'.format(user_home))

        # create a new xml file to store tag archive if doesn't already exist
        engine.XmlMachine.create_new_xml_file()

        # set version number from file
        with open('{}/VERSION.rst'.format(self.project_root)) as in_file:
            self.app_version = engine.sanitize_filter(in_file.read())[0:7]

        # create an instance of the TagEditor (which does the 'work')
        self.engine = engine.Engine()

        # # set up magic method to determine file mime type (for later)
        self.m = magic.open(magic.MAGIC_MIME_TYPE)
        self.m.load()

        ''' GLADE '''

        # # # TOP LEVEL GLADE SETUP
        self.glade_file = '{}/resources/iptceditor.glade'.format(self.project_root)
        # create builder and add the glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        # connect the signals
        self.builder.connect_signals(self)
        # get the top level glade object
        self.window = self.builder.get_object('main_window')

        # # CREATE INSTANCE REFERENCES TO WIDGETS
        self.about_dialog = None
        self.file_chooser_dialog = self.builder.get_object('file_chooser_dialog')
        self.file_chooser_widget = self.builder.get_object('file_chooser_widget')
        self.file_select_button = self.builder.get_object('file_select')
        self.file_chooser_status = self.builder.get_object('file_chooser_dialog_status_bar')
        self.file_selected_label = self.builder.get_object('tagger_current_dataset_label')
        self.file_selected_label_label = self.builder.get_object('tagger_current_dataset_label_label')
        self.preview_img = None
        self.activity_log = self.builder.get_object('activity_log')
        self.keyword_list_dialog = self.builder.get_object('keyword_list_dialog')
        self.keyword_selection_viewport = self.builder.get_object('keyword_dialog_viewport')
        self.keyword_selection_list = None
        self.keywords_selected = []
        self.active_img = self.builder.get_object('active_image')

        # # CREATE INSTANCE REFERENCES TO TEXT INPUT FIELDS (to allow clearing, etc)
        self.input_text_fields = [
            self.builder.get_object('tagger_new_keyword_input'),
            self.builder.get_object('tagger_keyword_to_replace_input'),
            self.builder.get_object('iptc_remove_field')
        ]

        # # create file chooser filter
        self.filechooser_filter = Gtk.FileFilter()
        self.filechooser_filter.set_name('Images')
        list(map(self.filechooser_filter.add_mime_type, data_reader.AcceptedFormats.FORMATS))

        # # store filename / directory
        self.filename = self.directory = None

        # SHOW THE MAIN WINDOW
        print('Showing window ...')
        self.window.show_all()

        # RUN THE GTK
        Gtk.main()

    # # # # GTK EVENT HANDLERS

    # # # MAIN WINDOW

    def on_main_window_destroy(self, object, data=None):
        print('Quit with Cancel ...')
        self.window.destroy()
        Gtk.main_quit()

    # # # MENU
    def on_gtk_about_activate(self, menuitem, data=None):
        # get the object and assign to the attribute
        self.about_dialog = self.builder.get_object('aboutdialog')
        # update version number in about info
        self.about_dialog.set_version(self.app_version)
        response = self.about_dialog.run()
        self.about_dialog.hide()

    def on_gtk_filechooser_activate(self, menuitem, data=None):
        # reset any previously used text input fields
        self.input_reset()
        # set status in status bar
        status_label = self.builder.get_object('file_chooser_dialog_file_selection').get_text()
        self.file_chooser_status.push(0, status_label)
        # set filter
        if not self.file_chooser_widget.get_filter():
            self.file_chooser_widget.add_filter(self.filechooser_filter)
        self.preview_img = self.builder.get_object('preview_image')
        # always start selecting FILE in user home directory
        self.file_chooser_widget.set_current_folder(os.getenv('USERPROFILE') or os.getenv('HOME'))
        self.file_chooser_widget.set_action(Gtk.FileChooserAction.OPEN)
        response = self.file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            print('File chooser OK')
        elif response == Gtk.ResponseType.CANCEL:
            self.preview_img.set_from_stock('gtk-missing-image', 6)  # reset preview image
            self.file_chooser_dialog.hide()
        self.preview_img.set_from_stock('gtk-missing-image', 6)  # reset preview image
        self.file_chooser_dialog.hide()

    # # # BUTTONS

    def on_about_dialog_cancel_clicked(self, button):
        self.about_dialog.hide()

    def on_file_chooser_button_clicked(self, button):
        current_view = self.file_chooser_widget.get_current_folder()
        if button == self.builder.get_object('choose_file_button'):
            # set status in status bar
            status_label = self.builder.get_object('file_chooser_dialog_file_selection').get_text()
            self.file_chooser_status.remove_all(0)  # clear previous
            self.file_chooser_status.push(0, status_label)
            for stat in self.file_chooser_status:
                print(stat)
            if not self.file_chooser_widget.get_filter():
                self.file_chooser_widget.add_filter(self.filechooser_filter)
            # hide select button
            self.file_chooser_widget.set_current_folder(
                current_view) if current_view else None  # reset to current folder
            self.file_chooser_widget.set_action(Gtk.FileChooserAction.OPEN)
            self.preview_img.set_from_stock('gtk-missing-image', 6)  # reset preview image to stock
        elif button == self.builder.get_object('choose_dir_button'):
            # set status in status bar
            status_label = self.builder.get_object('file_chooser_dialog_dir_selection').get_text()
            self.file_chooser_status.remove_all(0)  # clear previous
            self.file_chooser_status.push(0, status_label)
            if self.file_chooser_widget.get_filter():
                self.file_chooser_widget.remove_filter(self.filechooser_filter)  # remove filter for dir sel
            # display select button
            self.file_select_button.show()
            self.file_chooser_widget.set_current_folder(current_view) if current_view else None
            self.file_chooser_widget.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
            self.preview_img.set_from_stock('gtk-missing-image', 6)
        elif button == self.builder.get_object('close_file_chooser'):
            self.file_chooser_dialog.hide()

    def on_tagger_button_clicked(self, button):
        meta_dialog = self.builder.get_object('meta_dialog')  # get reference to the display dialog
        if button == self.builder.get_object('tagger_display_kw_button'):
            self.display_data(
                dataset=self.get_dataset(),
                mode=data_reader.Mode.KEYWORDS)  # call the method to display the keywords
            response = meta_dialog.run()
        elif button == self.builder.get_object('tagger_display_iptc_button'):
            self.display_data(
                dataset=self.get_dataset(),
                mode=data_reader.Mode.TAG_TYPES)  # call method to display iptc dataset
            response = meta_dialog.run()
        elif button == self.builder.get_object('tagger_display_iptc_date_button'):
            self.display_data(
                dataset=self.get_dataset(),
                mode=data_reader.Mode.DATE)  # call method to display iptc date data
            response = meta_dialog.run()
        elif button == self.builder.get_object('tagger_replace_kw_button'):
            self.replace_keywords(self.get_dataset())  # call method to replace the keywords
        elif button == self.builder.get_object('tagger_remove_iptc_button'):
            self.remove_iptc(self.get_dataset())
        elif button == self.builder.get_object('meta_dialog_close'):
            meta_dialog.hide()

    def on_keyword_to_replace_dialog_closed(self, button):
        # set the text to nowt
        input_field = self.builder.get_object('tagger_keyword_to_replace_input')
        input_field.set_text('')
        # destroy the list
        self.keyword_selection_list.destroy()
        # close the dialog
        self.keyword_list_dialog.hide()

    def on_keyword_to_replace_dialog_select(self, button):
        input_field = self.builder.get_object('tagger_keyword_to_replace_input')
        # grab the selected fields (code for multiple selections, in case want to modify to allow in future).
        self.keyword_selection_list.selected_foreach(self.retrieve_keyword)
        input_field.set_text(self.keywords_selected[0] if self.keywords_selected else '')
        del self.keywords_selected[:]
        self.keyword_selection_list.destroy()
        self.keyword_list_dialog.hide()

    # # # FILE CHOOSER WIDGET

    def on_file_chooser_selected(self, widget):
        if self.file_chooser_widget.get_action() == Gtk.FileChooserAction.OPEN:
            # set the filename in the tag editor if choosing a file
            self.filename = engine.sanitize_filter(self.file_chooser_widget.get_filename())
            self.directory = None
            # update the file selected label for the tagger
            self.file_selected_label_label.set_text(
                self.builder.get_object('tagger_file_selected').get_text())
            self.file_selected_label.set_text(self.filename)
            # add to log
            self.add_to_log(self.builder.get_object('log_file_selected'),
                            self.filename)
        elif self.file_chooser_widget.get_action() == Gtk.FileChooserAction.SELECT_FOLDER:
            # set the directory in the tag editor if choosing a directory
            self.directory = engine.sanitize_filter(self.file_chooser_widget.get_filename())
            self.filename = None
            # update the file selected label for the tagger
            self.file_selected_label_label.set_text(
                self.builder.get_object('tagger_dir_selected').get_text())
            self.file_selected_label.set_text(self.directory)
            # add to log
            self.add_to_log(self.builder.get_object('log_directory_selected'),
                            self.file_chooser_widget.get_filename())
        # set the active image in the tagger
        self.set_active_image()
        # hide the chooser dialog
        self.file_chooser_dialog.hide()

    def on_file_chooser_selection_changed(self, widget):
        # when selection changed, if mode is to select a file, prevent selection of dir
        sel = engine.sanitize_filter(self.file_chooser_widget.get_filename())
        if (sel and self.file_chooser_widget.get_action() == Gtk.FileChooserAction.OPEN and
                os.path.isdir(sel)):
            # self.file_chooser_widget.unselect_all()
            self.file_select_button.hide()
        elif (sel and self.file_chooser_widget.get_action() == Gtk.FileChooserAction.OPEN and
                  os.path.isfile(sel)):
            self.file_select_button.show()

    def on_file_chooser_update_preview(self, widget=None):
        filename = self.file_chooser_widget.get_filename()
        try:
            if self.m.file(filename) in data_reader.AcceptedFormats.FORMATS:
                self.preview_img.set_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_scale(filename,
                                                            300, -1, True))
        except Exception as e:
            pass

    # # # DYNAMIC INPUT FIELDS # # #

    def on_tagger_keyword_to_replace_input_activate(self, widget, event=None, userdata=None):
        keywords_in_dataset = self.display_data(dataset=self.get_dataset(),
                                                mode=data_reader.Mode.KEYWORDS)
        keywords_list = self.list_all_keywords(list_of_files_keyword_lists=keywords_in_dataset)
        if keywords_in_dataset:
            self.keyword_selection_list = self.build_keyword_selector(keywords_list=keywords_list)
            self.keyword_selection_viewport.add(self.keyword_selection_list)
            response = self.keyword_list_dialog.run()
            self.keyword_list_dialog.hide()

    def on_tagger_new_keyword_input_focus_in_event(self, widget, event=None, userdata=None):
        # get
        tagger_keywords_listbox = None
        tagger_scroller = self.builder.get_object('active_scroller')
        viewport = tagger_scroller.get_child()
        keywords_archive = engine.XmlMachine.get_keywords_from_xml()
        keyword_list = sorted(list(set(keywords_archive)), key=str.lower, reverse=True)
        # remove the image
        viewport.remove(viewport.get_child())
        if keyword_list:
            tagger_keywords_listbox = self.build_keyword_selector(keywords_list=keyword_list)
        if tagger_keywords_listbox:
            # add listbox to viewport
            viewport.add(tagger_keywords_listbox)
            # set selection to single
            tagger_keywords_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            # on row selected
            tagger_keywords_listbox.connect('row-activated', self.add_to_new_keyword_entry_field)
        else:
            label_text = self.builder.get_object('tagger_active_no_keywords_label').get_text()
            new_label = Gtk.Label()
            new_label.set_line_wrap(True)
            new_label.set_markup(label_text)
            new_label.set_valign(Gtk.Align.CENTER)
            viewport.add(new_label)

    def add_to_new_keyword_entry_field(self, row, data=None):
        # populate input field
        field = self.builder.get_object('tagger_new_keyword_input')
        if field.get_text():
            field.set_text('{}, {}'.format(field.get_text().strip(), row.get_selected_row().get_child().get_text()))
        else:
            field.set_text('{}'.format(row.get_selected_row().get_child().get_text()))

    def on_tagger_new_keyword_input_reinstate_image(self, widget):
        print('reinstating active image')
        tagger_scroller = self.builder.get_object('active_scroller')
        viewport = tagger_scroller.get_child()
        viewport.get_child().destroy()
        viewport.add(self.active_img)
        viewport.show_all()

    # # # # GUI UPDATING (work ...)

    def set_active_image(self):
        print('Setting active image ...')
        # get reference to the preview img and label
        default_img = '{}/resources/default.png'.format(self.project_root)
        active_img_box = self.builder.get_object('active_img_box')
        current_label = active_img_box.get_children()[0]
        # # if single file
        if self.filename and not self.directory:
            # set image
            if data_reader.image_extension_checker(self.filename):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.filename, -1, 300, True)
                self.active_img.set_from_pixbuf(pixbuf)
        # # if directory
        elif self.directory and not self.filename:
            directory = '{}/'.format(engine.sanitize_filter(self.directory))  # get dir and add trailing slash
            file_list = [engine.sanitize_filter(file) for file in os.listdir(directory)
                         if os.path.isfile('{}{}'.format(directory, file)) and
                         self.m.file('{}{}'.format(directory, file)) in data_reader.AcceptedFormats.FORMATS]
            if file_list:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    '{}{}'.format(directory, file_list[0]), -1, 300, True)
                self.active_img.set_from_pixbuf(pixbuf)
            else:
                pass
                self.active_img.set_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_scale(default_img,
                                                            -1, 300, True))

    def display_data(self, dataset=None, mode=None):
        result = data_reader.DataReader.get_tags(new_keyword_list=None,
                                                 dataset=dataset,
                                                 mode=mode) or None  # returns list of lists
        meta_label = self.builder.get_object('meta_label')
        no_results_label = self.builder.get_object('meta_label_blurb_3').get_text()
        results_string = self.make_results_str(result) or no_results_label
        # log it
        if results_string:
            if mode == data_reader.Mode.KEYWORDS:
                self.add_to_log(self.builder.get_object('log_keywords_displayed'))
            elif mode == data_reader.Mode.TAG_TYPES:
                self.add_to_log(self.builder.get_object('log_iptc_dataset_displayed'))
            elif mode == data_reader.Mode.DATE:
                self.add_to_log(self.builder.get_object('log_iptc_date_displayed'))
        else:
            if mode == data_reader.Mode.KEYWORDS:
                self.add_to_log(self.builder.get_object('log_keywords_display_failed'))
            elif mode == data_reader.Mode.TAG_TYPES:
                self.add_to_log(self.builder.get_object('log_iptc_dataset_display_failed'))
            elif mode == data_reader.Mode.DATE:
                self.add_to_log(self.builder.get_object('log_iptc_date_display_failed'))
        # create the data label
        meta_label.set_markup(results_string)
        # submit keywords that are pulled from dataset to xml, in case any are new
        if result:
            #engine.XmlMachine.add_xml_tags((', '.join([', '.join(l[:-1]) for l in result])).split(', '))
            tags = []
            for e in (l[:-1] for l in result):
                tags += e
            engine.XmlMachine.add_xml_tags(tags)
        # return the result list to calling method, for work, if necessary
        return result

    def replace_keywords(self, dataset=None):
        new_keywords = self.builder.get_object('tagger_new_keyword_input').get_text()
        # create list from above comma separated string for multiple new keywords
        new_keyword_list = self.create_new_keywords_list_from_string(keyword_string=new_keywords)
        old_keyword = self.builder.get_object('tagger_keyword_to_replace_input').get_text()
        # clear input fields for next time
        self.clear_all_inputs()
        # replace!
        if self.engine.replace_keywords(dataset=dataset,
                                        keyword_to_replace=old_keyword,
                                        new_keywords=new_keyword_list) is not False:
            self.add_to_log(self.builder.get_object('log_added_keyword'),
                            [old_keyword, ", ".join(new_keyword_list) if new_keyword_list else ""])
            return True
        self.add_to_log(self.builder.get_object('log_keyword_replace_failed'))
        return False

    def clear_all_inputs(self):
        self.builder.get_object('tagger_new_keyword_input').set_text('')
        self.builder.get_object('tagger_keyword_to_replace_input').set_text('')
        self.builder.get_object('iptc_remove_field').set_text('')
        return True

    def remove_iptc(self, dataset=None):
        iptc_dataset_to_remove = self.builder.get_object('iptc_remove_field').get_text()
        if iptc_dataset_to_remove:
            if self.engine.remove_exif_field(dataset, [iptc_dataset_to_remove]):
                self.add_to_log(self.builder.get_object('log_iptc_dataset_removed'))
                return True
        self.add_to_log(self.builder.get_object('log_iptc_dataset_removal_error'))

    # # # # HELPERS

    def create_new_keywords_list_from_string(self, keyword_string=None):
        if keyword_string:
            # make list
            new_keyword_list_unclean = keyword_string.strip().split(", ")
            # return (limit to 10 keywords to avoid memory foolishness)
            return [engine.sanitize_filter(kw) for kw in new_keyword_list_unclean[:10]] or None
        return None

    def get_dataset(self):
        if self.filename:
            return ['F', self.filename]
        elif self.directory:
            return ['D', self.directory]
        else:
            return None

    def make_results_str(self, input_list=None):
        # input list is list of lists of keywords for each file
        blurb_1 = self.builder.get_object('meta_label_blurb_1').get_text()
        blurb_2 = self.builder.get_object('meta_label_blurb_2').get_text()
        if input_list:
            res_str = ''
            for r in input_list:
                res_str += '{} "{}" {}\n{}\n\n'.format(blurb_1, r[-1], blurb_2, ' | '.join(r[:-1]))
            return res_str

    def add_to_log(self, label, incoming=None):
        # if incoming is a list (and it's not empty!), join into a string
        data = ' > '.join(incoming) if isinstance(incoming, list) else incoming
        if type(label) == Gtk.Label:
            label_message = label.get_text()
            new_label = Gtk.Label('{} {}'.format(label_message, data if data else ''))
            new_label.set_selectable(True)
            new_label.set_halign(Gtk.Align.START)
            new_label.set_padding(3, 3)
            new_row = Gtk.ListBoxRow()
            new_row.add(new_label)
            self.activity_log.prepend(new_row)
            self.activity_log.show_all()
        else:
            print('A message Label has not been passed!')

    @staticmethod
    def build_keyword_selector(keywords_list=None):
        if keywords_list:
            keyword_selection_list = Gtk.ListBox()
            keyword_selection_list.set_activate_on_single_click(False)
            keyword_selection_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
            for keyword in keywords_list:
                new_label = Gtk.Label(keyword)
                new_label.set_selectable(False)
                new_label.set_halign(Gtk.Align.START)
                new_label.set_padding(3, 3)
                new_row = Gtk.ListBoxRow()
                new_row.add(new_label)
                keyword_selection_list.prepend(new_row)
            keyword_selection_list.show_all()
            return keyword_selection_list
        else:
            return None

    @staticmethod
    def list_all_keywords(list_of_files_keyword_lists=None):
        if not list_of_files_keyword_lists: return False
        keyword_list = []
        for file_keyword_list in list_of_files_keyword_lists:
            file_keyword_list.pop()  # pop off the filename - we don't need that
            keyword_list += file_keyword_list
        return sorted(list(set(keyword_list)), key=str.lower)

    def retrieve_keyword(self, widget, row, data=None):
        self.keywords_selected.append(row.get_child().get_text())

    def input_reset(self):
        for field in self.input_text_fields:
            field.set_text('')
        return True


if __name__ == '__main__':
    GuiGtkGlade()
