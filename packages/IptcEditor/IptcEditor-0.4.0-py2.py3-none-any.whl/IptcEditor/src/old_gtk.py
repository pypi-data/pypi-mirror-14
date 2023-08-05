import gi, os, magic, webbrowser

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from datetime import datetime
from IptcEditor.src.engine import Engine


class GtkGui(Gtk.Window):
    def __init__(self):

        self.DOCS_URL = 'https://github.com/ZWS2014/python-iptceditor-gtk3/blob/master/IptcEditor/README.rst#usage'

        # project_root = os.path.dirname(os.path.realpath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(__file__))

        # # create instance of the editor
        self.editor = Engine()

        # # set default image
        self.default_image = '{}/resources/default.png'.format(self.project_root)

        # # set up variables[self.remove_field_input.get_text()]
        self.activity_log_label = Gtk.Label()  # make class attribute, for updating
        self.thumbnail_width = 0
        self.thumbnail_height = 0
        self.thumbnail = Gtk.Image()  # make class attribute, for updating
        self.thumbnail_title = Gtk.Label()  # class attribute, for updating

        # # create activity log list
        self.activity_log = []

        # # set default thumbnail size
        # self.set_thumbnail_width(175)
        self.set_thumbnail_height(250)

        # # # init the window object, passing the title
        Gtk.Window.__init__(self, title='IPTC Tag Modifier')

        # # set default window size
        self.set_default_size(1024, 968)

        # # call my set_header method
        self.set_header()

        # # call my set_main_window method
        self.set_main_window()

    def set_header(self):

        # # set header bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        # # add title to header bar
        header_bar.props.title = 'IPTC Editor'
        # # create buttons for header bar
        docs_button = Gtk.Button()
        docs_button.connect('clicked', self.docs_button_clicked)
        # # create icons for the buttons
        # docs_button_icon = Gio.ThemedIcon(name='gtk-about')
        # docs_button_icon_img = Gtk.Image.new_from_gicon(docs_button_icon, Gtk.IconSize.BUTTON)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            '{}/resources/web-browser.png'.format(self.project_root),
            16, -1, True)
        docs_button_icon_img = Gtk.Image()
        docs_button_icon_img.set_from_pixbuf(pixbuf)
        # # create labels for the buttons
        docs_button_label = Gtk.Label()
        docs_button_label.set_markup('<small>Online Docs</small>')
        # # create boxes for the button labels and icons
        docs_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        docs_button_box.set_valign(Gtk.Align.END)
        docs_button_box.set_homogeneous(False)
        # # pack the labels and icons into the boxes
        docs_button_box.pack_end(docs_button_icon_img, True, True, 0)
        docs_button_box.pack_end(docs_button_label, True, True, 0)
        # # add the boxes to the buttons
        docs_button.add(docs_button_box)
        # # create box for header bar buttons
        header_buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_buttons_box.set_valign(Gtk.Align.START)
        header_buttons_box.set_homogeneous(False)
        header_buttons_box.pack_end(docs_button, True, True, 0)
        header_bar.pack_end(header_buttons_box)
        # # add header bar to title bar
        self.set_titlebar(header_bar)

    def set_main_window(self):

        # # create notebook
        self.set_border_width(10)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # # add 'pages' to the notebook
        self.notebook.append_page(self.nb_page_1(), Gtk.Label('Source Selection'))
        self.notebook.append_page(self.nb_page_2(), Gtk.Label('Tagger'))

    def nb_page_1(self):

        # # set up initial variables
        file_label_text = 'Image file ...'
        directory_label_text = 'Image directory, for bulk operations ...'

        # # create page boxes
        self.page_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.page_1.set_border_width(10)

        # # create buttons
        self.file_button = Gtk.Button(label='Choose a file')
        self.file_button.connect('clicked', self.file_selector)
        self.directory_button = Gtk.Button(label='Choose a directory (for bulk operations)')
        self.directory_button.connect('clicked', self.directory_selector)

        # # create labels
        self.file_label = Gtk.Label()
        self.directory_label = Gtk.Label()
        self.file_label.set_markup('<small>{txt}</small>'.format(txt=file_label_text))
        self.file_label.set_justify(Gtk.Justification.LEFT)
        self.file_label.set_line_wrap(True)
        self.directory_label.set_markup('<small>{txt}</small>'.format(txt=directory_label_text))
        self.directory_label.set_justify(Gtk.Justification.LEFT)
        self.directory_label.set_line_wrap(True)
        self.or_label = Gtk.Label()
        self.or_label.set_markup('<small><i>Or</i></small>')
        self.or_label.set_justify(Gtk.Justification.CENTER)

        # # create a grid
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_column_homogeneous(False)

        # # add button to grid as first reference object
        self.grid.add(self.file_button)

        # # attach other objects (labels & buttons) to the grid
        self.grid.attach(self.file_label, 1, 0, 2, 1)
        self.grid.attach(self.or_label, 0, 1, 1, 1)
        self.grid.attach(self.directory_button, 0, 2, 1, 1)
        self.grid.attach(self.directory_label, 1, 2, 2, 1)

        # # add grid to page
        self.page_1.pack_start(self.grid, True, True, 0)

        # # return the page
        return self.page_1

    def nb_page_2(self):

        # # create page boxes
        page_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page_2.set_border_width(10)

        # # create the page's grid
        tagger_grid = Gtk.Grid()
        tagger_grid.set_row_spacing(10)
        tagger_grid.set_column_spacing(10)
        tagger_grid.set_column_homogeneous(False)
        tagger_grid.set_row_homogeneous(False)

        # # create labels
        old_tag_label = Gtk.Label()
        new_tag_label = Gtk.Label()
        remove_field_label = Gtk.Label()
        activity_log_title = Gtk.Label()
        thumbnail_no_img = Gtk.Label()
        old_tag_label.set_markup('<b>Keyword to replace</b>')
        old_tag_label.set_halign(Gtk.Align.START)
        new_tag_label.set_markup('<b>New keyword</b>')
        new_tag_label.set_halign(Gtk.Align.START)
        remove_field_label.set_markup('<b>IPTC dataset to remove</b>')
        remove_field_label.set_halign(Gtk.Align.START)
        activity_log_title.set_markup('<u><b><big>Activities This Session</big></b></u>')
        activity_log_title.set_valign(Gtk.Align.START)
        activity_log_title.set_halign(Gtk.Align.START)
        thumbnail_no_img.set_markup('<small><b>There is no image to display</b></small>')
        thumbnail_no_img.set_valign(Gtk.Align.START)
        thumbnail_no_img.set_halign(Gtk.Align.START)
        self.thumbnail_title.set_valign(Gtk.Align.START)
        self.thumbnail_title.set_halign(Gtk.Align.START)
        self.activity_log_label.set_valign(Gtk.Align.START)
        self.activity_log_label.set_halign(Gtk.Align.START)
        self.activity_log_label.set_line_wrap(True)

        # # create buttons
        display_iptc_kw_button = Gtk.Button('Display Keywords')
        display_iptc_kw_button.connect('clicked', self.display_kw_clicked)
        display_iptc_tags_button = Gtk.Button('Display IPTC Datasets')
        display_iptc_tags_button.connect('clicked', self.display_tagtypes_clicked)
        display_date_button = Gtk.Button('Display Date Created')
        display_date_button.connect('clicked', self.display_date_button_clicked)
        replace_button = Gtk.Button('Replace keyword(s)')
        replace_button.connect('clicked', self.replace_clicked)
        remove_button = Gtk.Button('Remove IPTC Dataset')
        remove_button.connect('clicked', self.remove_clicked)

        # # create labels for button box sections
        display_buttons_label = Gtk.Label()
        action_buttons_label = Gtk.Label()
        display_buttons_label.set_markup('<u><b>Display Options</b></u>')
        action_buttons_label.set_markup('<u><b>Action Options</b></u>')

        # # create box for display buttons
        display_buttons_box = Gtk.VButtonBox(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        display_buttons_box.set_valign(Gtk.Align.START)
        display_buttons_box.set_halign(Gtk.Align.START)
        display_buttons_box.set_homogeneous(True)
        # add label to box
        display_buttons_box.pack_start(display_buttons_label, True, True, 0)
        # add display buttons to box
        display_buttons_box.pack_start(display_iptc_kw_button, True, True, 0)
        display_buttons_box.pack_start(display_date_button, True, True, 0)
        display_buttons_box.pack_start(display_iptc_tags_button, True, True, 0)

        # # create box for action buttons
        action_buttons_box = Gtk.VButtonBox(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        action_buttons_box.set_valign(Gtk.Align.START)
        action_buttons_box.set_halign(Gtk.Align.START)
        action_buttons_box.set_homogeneous(True)
        # add label to box
        action_buttons_box.pack_start(action_buttons_label, True, True, 0)
        # add action buttons to box
        action_buttons_box.pack_start(replace_button, True, True, 0)
        action_buttons_box.pack_start(remove_button, True, True, 0)

        # # create container box for action and display buttons
        buttons_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        buttons_container.set_halign(Gtk.Align.START)
        buttons_container.set_valign(Gtk.Align.START)
        buttons_container.set_homogeneous(True)
        # # add button boxes to container box
        buttons_container.pack_start(display_buttons_box, True, True, 0)
        buttons_container.pack_start(action_buttons_box, True, True, 0)

        # # create scrolled window for thumbnail, grab image & create thumb, and add to the window
        thumbnail_window = Gtk.ScrolledWindow()
        thumbnail_window.set_hexpand(True)
        thumbnail_window.set_vexpand(True)
        # # set the thumbnail
        self.set_thumbnail()
        # # create containing box
        thumbnail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        thumbnail_box.set_valign(Gtk.Align.START)
        thumbnail_box.set_halign(Gtk.Align.START)
        thumbnail_box.set_homogeneous(False)
        # # add title and thumbnail to the box
        thumbnail_box.pack_start(self.thumbnail_title, True, True, 0)
        thumbnail_box.pack_start(self.thumbnail, True, True, 0)
        thumbnail_box.set_valign(Gtk.Align.START)
        thumbnail_box.set_halign(Gtk.Align.START)
        # # add the box to the window
        thumbnail_window.add_with_viewport(thumbnail_box)

        # # create input fields
        self.tag_to_replace = Gtk.Entry()
        self.tag_to_replace.set_hexpand(True)
        self.new_tag_input = Gtk.Entry()
        self.remove_field_input = Gtk.Entry()

        # # create scroller for operation messages
        message_scroller = Gtk.ScrolledWindow()
        message_scroller.set_hexpand(True)
        message_scroller.set_vexpand(True)

        # # create spacer box
        spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        spacer.set_valign(Gtk.Align.START)

        # # create box for the activity log
        activity_log_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        activity_log_container.set_valign(Gtk.Align.START)

        # # add the labels to the box
        activity_log_container.pack_start(self.activity_log_label, True, True, 0)

        # # update the list and add to the label
        self.add_to_log('Awaiting instruction ...')

        # # add the box to the scroller
        message_scroller.add_with_viewport(activity_log_container)

        # # add the labels and input fields to the grid
        tagger_grid.attach(buttons_container, 0, 0, 1, 1)
        tagger_grid.attach(thumbnail_window, 1, 0, 3, 1)
        tagger_grid.attach(new_tag_label, 0, 1, 1, 1)
        tagger_grid.attach(self.new_tag_input, 1, 1, 3, 1)
        tagger_grid.attach(old_tag_label, 0, 2, 1, 1)
        tagger_grid.attach(self.tag_to_replace, 1, 2, 3, 1)
        tagger_grid.attach(remove_field_label, 0, 3, 1, 1)
        tagger_grid.attach(self.remove_field_input, 1, 3, 3, 1)
        tagger_grid.attach(spacer, 0, 4, 4, 2)
        tagger_grid.attach(activity_log_title, 0, 6, 4, 1)
        tagger_grid.attach(message_scroller, 0, 7, 4, 3)

        # # add the grid to the page box
        page_2.pack_start(tagger_grid, True, True, 0)

        # # return the page
        return page_2

    def set_thumbnail_width(self, w):
        self.thumbnail_width = w

    def set_thumbnail_height(self, h):
        self.thumbnail_height = h

    def set_thumbnail(self):
        pixbuf = None
        fn = self.editor.get_filename()
        dn = self.editor.get_directory()
        # # set up magic method to determine file mime type (for later)
        m = magic.open(magic.MAGIC_MIME_TYPE)
        m.load()
        # # if single file
        if fn and not dn:
            # set thumbnail title
            self.thumbnail_title.set_markup('<small><b>Chosen image preview</b></small>')
            # set thumbnail image
            if m.file(fn) in self.editor.get_accepted_formats():
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(fn, -1, self.thumbnail_height, True)
        # # if directory
        elif dn:
            # set thumbnail title
            self.thumbnail_title.set_markup('<small><b>Preview of image in selected directory</b></small>')
            # set thumbnail image (first image of accepted format)
            wd = self.editor.get_directory().rstrip('/')
            os.chdir(wd)
            file_list = [file for file in os.listdir(wd) if os.path.isfile(file) and
                         m.file(file) in self.editor.get_accepted_formats()]
            if file_list:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(file_list[0], -1, self.thumbnail_height, True)
        if pixbuf:
            self.thumbnail.set_from_pixbuf(pixbuf)
        else:
            self.thumbnail.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.default_image,
                                                        -1, self.thumbnail_height, True))

    def add_to_log(self, log_message=None):
        if log_message:
            time = datetime.now().strftime('%H:%M:%S')
            label = ''
            self.activity_log.append('<small>{0}</small>: <big><i>{1}</i></big>'.format(time, log_message))
            rev = reversed(self.activity_log)
            label += '\n\n'.join(rev)
            self.activity_log_label.set_markup(label)
        else:
            return False

    # select select select ...

    def file_selector(self, widget):
        dialog = Gtk.FileChooserDialog('Please select the image file',
                                       self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_label.set_markup('<small><b>{txt}</b></small>'.format(txt=dialog.get_filename()))
            self.directory_label.set_markup('<small><b>A single file selected.</b></small>')
            # get the filename from the file chooser dialog
            self.editor.set_filename(dialog.get_filename())
            self.editor.set_directory(None)  # ensure directory is reset to None to prevent selecting both file & dir
            # set the thumb
            self.set_thumbnail()
            # # log activity
            self.add_to_log('File "{0}" selected for operation.'.format(dialog.get_filename()))
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def directory_selector(self, widget):
        dialog = Gtk.FileChooserDialog('Please select the image files directory for bulk operations',
                                       self, Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.directory_label.set_markup('<small><b>{txt}</b></small>'.format(txt=dialog.get_filename()))
            self.file_label.set_markup('<small><b>A directory has been selected.</b></small>')
            self.editor.set_directory(dialog.get_filename())
            self.editor.set_filename(None)  # ensure file is reset to None to prevent selecting both file & dir
            # set the thumb
            self.set_thumbnail()
            # # log the activity
            self.add_to_log('Directory "{0}" selected for operation.'.format(dialog.get_filename()))
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    # clickety click ...

    def docs_button_clicked(self, button):
        webbrowser.open(self.DOCS_URL)

    def display_kw_clicked(self, button):
        # # create popup
        dialog = self.DialogPopup(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        # # write to activity log
        self.add_to_log('Keywords displayed.')

    def display_date_button_clicked(self, button):
        dialog = self.DialogPopup(self, type='Date')
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        self.add_to_log('ITPC Dates of Creation Displayed')

    def display_tagtypes_clicked(self, button):
        # # create popup
        dialog = self.DialogPopup(self, type='Tags')
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        # # write to activity log
        self.add_to_log('IPTC datasets displayed.')

    def replace_clicked(self, button):
        # set the filename / directory name
        working_data = ('F', self.editor.get_filename()) if self.editor.get_filename() \
            else ('D', self.editor.get_directory())
        new_keyphrase_list = [self.new_tag_input.get_text()]
        # grab the keyword tags and replace them
        tags = self.editor.get_tags(new_keyphrase_list, self.editor.get_filename(),
                                    self.editor.get_directory()) if new_keyphrase_list else None
        if self.editor.replace_keywords(existing_keyword_string_list=tags,
                                        new_kp_list=new_keyphrase_list,
                                        dataset=working_data,
                                        old_keyword=self.tag_to_replace.get_text(),
                                        new_keyword=self.new_tag_input.get_text()) is not False:
            self.add_to_log('Replaced key phrase "{0}" with "{1}"'.format(self.tag_to_replace.get_text(),
                                                                          self.new_tag_input.get_text()))
            return True
        self.add_to_log('Tag replacement failed.')
        return False

    def remove_clicked(self, button):
        if self.remove_field_input.get_text():
            ftr = [self.editor.my_filter(fields) for fields in [self.remove_field_input.get_text()]]
            if self.editor.remove_exif_field(ftr):
                self.add_to_log('IPTC field(s) removed.')
        else:
            self.add_to_log('IPTC field removal failed.')

    class DialogPopup(Gtk.Dialog):
        def __init__(self, parent, type='Keywords'):
            # note: set parent to "parent" to attach popup to main window (it's parent).
            Gtk.Dialog.__init__(self, 'IPTC Data',
                                parent=parent,
                                flags=Gtk.DialogFlags.MODAL,
                                buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))
            self.set_default_size(1024, 768)
            self.set_border_width(30)
            results_string = ''
            blurb = ''
            # grab the keywords or tags
            if type == 'Tags':
                parent.editor.set_mode('TAG_TYPES')
                blurb = '<b>Below are the IPTC datasets associated with the filenames indicated. ' \
                        'Datasets are separated by the | character.</b>'
            elif type == 'Keywords':
                parent.editor.set_mode('KEY_PHRASES')
                blurb = '<b>Below are the keywords associated with the filenames indicated. ' \
                        'Keywords are separated by the | character.</b>'
            elif type == 'Date':
                parent.editor.set_mode('DATE')
                blurb = '<b>Below are the "dates of creation" associated with the filenames indicated. ' \
                        'Dates are separated by the | character.</b>'
            result = parent.editor.get_tags(filename=parent.editor.get_filename(),
                                            directory=parent.editor.get_directory()) or None
            # create the string to display from the results list
            results_string = self.make_results_str(result) or 'There are no results to display!'
            blurb_label = Gtk.Label()
            blurb_label.set_markup(blurb)
            blurb_label.set_selectable(False)
            blurb_label.set_line_wrap(True)
            # write the content label
            label = Gtk.Label()
            label.set_markup(results_string)
            label.set_selectable(True)
            label.set_line_wrap(True)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
            box.set_valign(Gtk.Align.START)
            box.set_homogeneous(False)
            box.pack_start(blurb_label, True, True, 0)
            box.pack_start(label, True, True, 0)
            scroller = Gtk.ScrolledWindow()
            scroller.set_hexpand(True)
            scroller.set_vexpand(True)
            scroller.add_with_viewport(box)
            # create content area and add the label
            area = self.get_content_area()
            area.add(scroller)
            self.show_all()
            # return mode to default
            parent.editor.set_mode()

        @staticmethod
        def make_results_str(input_list=None):
            if input_list:
                res_str = ''
                for r in input_list:
                    res_str += 'Image name "<b><i>{0}</i></b>" ' \
                               'has the following: <b>| <i>{1}</i></b>\n'.format(
                        r[-1], ' </i>|<i> '.join(r[:-1]))
                return res_str
