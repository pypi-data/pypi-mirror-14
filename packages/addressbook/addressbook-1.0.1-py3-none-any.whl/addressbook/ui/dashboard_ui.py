# The MIT License (MIT)
#
# Copyright (c) 2016 Adam York
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import datetime
from operator import attrgetter
from tkinter import messagebox

from addressbook.data.create import create_comment
from addressbook.data.delete import delete_address
from addressbook.data.delete import delete_contact
from addressbook.data.delete import delete_identification
from addressbook.data.delete import delete_person
from addressbook.data.delete import delete_relationship
from addressbook.data.read import read_addresses
from addressbook.data.read import read_comment
from addressbook.data.read import read_email_contacts
from addressbook.data.read import read_identification
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.data.read import read_people
from addressbook.data.read import read_phone_contacts
from addressbook.data.read import read_relationships
from addressbook.data.read import search_people_1
from addressbook.data.read import search_people_2
from addressbook.data.update import update_address
from addressbook.data.update import update_comment
from addressbook.data.update import update_identification
from addressbook.data.update import update_person
from addressbook.models.addresses import Address
from addressbook.models.contacts import Email
from addressbook.models.contacts import Phone
from addressbook.models.identities import Identity
from addressbook.models.people import Comment
from addressbook.models.people import Person
from addressbook.models.people import Relationship
from addressbook.models.recordeventtypes import *
from addressbook.ui import about_ui
from addressbook.ui import address_ui
from addressbook.ui import email_ui
from addressbook.ui import help_ui
from addressbook.ui import identity_ui
from addressbook.ui import person_ui
from addressbook.ui import phone_ui
from addressbook.ui import relation_ui
from addressbook.ui.controls import *
from addressbook.ui.controls import sort_by_column
from addressbook.settings import size_dashboard_ui


class DashboardUi:
    """ Main address book dashboard"""
    def __init__(self, top_level):
        self.top_level = top_level
        self.top_level.wm_title("Address Book")

        # GLOBALS
        self.tree_person_row_iid = None

        # Class objects for passing to UI controls
        self.selected_email_record = Email()
        self.selected_phone_record = Phone()
        self.selected_relation_record = Relationship()

        # Child Windows
        self.relationship_child_top_level = None

        # Frames
        self.body_frame = Frame(self.top_level)
        self.header_frame = Frame(self.body_frame)
        self.center_frame = Frame(self.body_frame)
        self.footer_frame = Frame(self.body_frame)

        # self.customFont = Font(family="Helvetica", size=12)
        # Tree View
        self.tree_person = Treeview(self.center_frame, height=7, columns=("firstname", "lastname", "middleinitial",
                                                                          "nickname", "dateofbirth", "dateofdeath"))
        # Labels
        self.label_footer = Label(self.footer_frame, text="Footer")

        # Menus
        self.menu_bar = Menu()
        self.record_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.selected_record_menu = Menu(self.menu_bar, tearoff=0)

        # Search Bar
        self.header_frame.columnconfigure(0, weight=0)
        self.header_frame.columnconfigure(1, weight=0)
        self.header_frame.columnconfigure(2, weight=0)
        self.header_frame.columnconfigure(3, weight=5)
        self.header_frame.columnconfigure(4, weight=0)

        self.search_inputs = SearchInputs(self.header_frame)
        self.search_labels = SearchLabels(self.header_frame)
        self.search_inputs.search_button.configure(command=self.get_search_results)

        # Notebook Tabs
        self.notebook = Notebook(self.footer_frame, padding=0)
        self.person_tab_frame = Frame(self.notebook, width=600, height=300)
        self.person_tab_frame.columnconfigure(10, weight=12)

        self.address_tab_frame = Frame(self.notebook, width=600, height=300)
        self.address_tab_frame.columnconfigure(1, weight=3)

        self.identification_tab_frame = Frame(self.notebook, width=600, height=300)
        self.identification_tab_frame.columnconfigure(1, weight=3)

        self.relationship_tab_frame = Frame(self.notebook, width=600, height=300)
        self.relationship_tab_frame.columnconfigure(1, weight=2)

        self.comments_tab_frame = Frame(self.notebook, width=600, height=300)
        self.comments_tab_frame.columnconfigure(1, weight=2)

        self.tree_relationships = Treeview(self.relationship_tab_frame,
                                           columns=("firstname",
                                                    "lastname", "middleinitial",
                                                    "typedescription"))

        self.tree_phone_numbers = Treeview(self.person_tab_frame, height=3,
                                           columns=("personid", "contactid", "phonenumber", "sequenceno",
                                                    "typecode", "typedescription", "typeid"))

        self.tree_email = Treeview(self.person_tab_frame, height=5,
                                   columns=("personid", "contactid", "emailaddress",
                                            "sequenceno", "typeid", "typecode", "typedescription"))

        self.tree_addresses = Treeview(self.address_tab_frame, height=3,
                                       columns=("addressline1", "addressline2", "pobox", "city", "state",
                                                "zipcode", "zip4", "postalcode", "status", "typeid",
                                                "sequenceno", "typecode", "typedescription"))

        self.tree_identities = Treeview(self.identification_tab_frame, height=3,
                                        columns=("identificationnumber", "identificationtypeid",
                                                 "issuingauthority", "issuingentity",
                                                 "recordlocation", "typecode", "typedescription"))

        # Tree view (notebook tabs) row identifiers (iid)
        self.tree_address_row_iid = None
        self.tree_identity_row_iid = None
        self.tree_phone_row_iid = None
        self.tree_email_row_iid = None
        self.tree_relationship_row_iid = None

        # Buttons
        self.button_save_changes = Button(self.body_frame, text="Save Changes",
                                          command=self.save_dashboard_changes)
        self.button_delete_phone = Button(self.person_tab_frame, text="Delete Phone",
                                          command=lambda: self.delete_record(DeleteRecord.phone))
        self.button_delete_email = Button(self.person_tab_frame, text="Delete Email",
                                          command=lambda: self.delete_record(DeleteRecord.email))
        self.button_edit_phone = Button(self.person_tab_frame, text="Edit Phone",
                                        command=lambda: self.open_phone_ui(EditRecord.phone))
        self.button_edit_email = Button(self.person_tab_frame, text="Edit Email",
                                        command=lambda: self.open_email_ui(EditRecord.email))
        self.button_delete_relation = Button(self.relationship_tab_frame, text="Delete Relation",
                                             command=lambda: self.delete_record(DeleteRecord.relation))
        self.button_delete_address = Button(self.address_tab_frame, text="Delete Address",
                                            command=lambda: self.delete_record(DeleteRecord.address))
        self.button_delete_identification = Button(self.identification_tab_frame, text="Delete Identification",
                                                   command=lambda: self.delete_record(DeleteRecord.identification))

        # Frames belonging to notebook (children frames)
        self.person_field_frame = Frame(self.person_tab_frame)
        self.address_field_frame = Frame(self.address_tab_frame)
        self.identity_field_frame = Frame(self.identification_tab_frame)

        self.button_delete_person = Button(self.person_field_frame, text="Delete Person",
                                           command=lambda: self.delete_record(DeleteRecord.person))

        # Entry and Label widgets belonging to tab frames
        # Person
        self.person_labels = PersonLabels(self.person_field_frame)
        self.person_inputs = PersonInputs(self.person_field_frame)
        # Address
        self.address_labels = AddressLabels(self.address_field_frame)
        self.address_inputs = AddressInputs(self.address_field_frame)
        # Identity
        self.identity_inputs = IdentityInputs(self.identity_field_frame)
        self.identity_labels = IdentityLabels(self.identity_field_frame)
        # Comments
        self.comment_inputs = CommentsInputs(self.comments_tab_frame)

        # Dashboard choices (options) for tabs with options
        self.address_codes = []
        self.address_type_list = self.get_address_codes()
        self.address_type_list.insert(0, "PLEASE-SELECT")
        self.address_type_option_variable = StringVar(top_level)
        self.address_type_options = OptionMenu(self.address_field_frame, self.address_type_option_variable,
                                               *self.address_type_list)

        self.identity_codes = []
        self.identity_type_list = self.get_id_codes()
        self.identity_type_option_variable = StringVar(top_level)
        self.identity_type_options = OptionMenu(self.identity_field_frame, self.identity_type_option_variable,
                                                *self.identity_type_list, command=self.set_identification_type_id)
        # Scroll Bars
        self.person_scroll_bar = Scrollbar(self.center_frame)
        self.address_scroll_bar = Scrollbar(self.address_tab_frame)
        self.phone_scroll_bar = Scrollbar(self.person_tab_frame)
        self.email_scroll_bar = Scrollbar(self.person_tab_frame)
        self.identities_scroll_bar = Scrollbar(self.identification_tab_frame)
        self.relationship_scroll_bar = Scrollbar(self.relationship_tab_frame)
        self.comments_scroll_bar = Scrollbar(self.comments_tab_frame)

    def apply_layout(self):
        """Applies UI layout"""

        # Set window size
        self.top_level.geometry(size_dashboard_ui)

        # Create commands for the record menu
        self.record_menu.add_command(label="Person Record", command=lambda: self.open_person_ui("insert"))

        # Add the menu bar and its commands.
        self.menu_bar.add_cascade(label="New", menu=self.record_menu)

        # Add the menu for the selected record
        self.selected_record_menu.add_command(label="Add Address", command=self.open_address_ui)

        self.selected_record_menu.add_command(label="Add Email", command=lambda: self.open_email_ui(CreateRecord.email))
        self.selected_record_menu.add_command(label="Add Phone", command=lambda: self.open_phone_ui(CreateRecord.phone))
        self.selected_record_menu.add_command(label="Add Identity", command=self.open_identity_ui)
        self.selected_record_menu.add_command(label="Add Relationship", command=self.open_relation_ui)
        self.selected_record_menu.add_separator()
        self.selected_record_menu.add_command(label="Delete", command=lambda: self.delete_record(DeleteRecord.person))
        self.menu_bar.add_cascade(label="Selected Person", menu=self.selected_record_menu)

        # Add the help menu bar and its commands to the main menu bar.
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About...", command=self.open_about_ui)
        self.help_menu.add_command(label="Show Help.", command=self.open_help_ui)

        # Display the menu bar with all of its other menus.
        self.top_level.config(menu=self.menu_bar)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)
        Grid.columnconfigure(self.body_frame, 1, weight=1)
        Grid.columnconfigure(self.header_frame, 1, weight=1)
        Grid.columnconfigure(self.center_frame, 1, weight=1)
        Grid.columnconfigure(self.footer_frame, 1, weight=1)

        # Frames
        self.body_frame.grid(row=0, column=0, columnspan=10, sticky=EW)
        self.header_frame.grid(row=1, column=0, columnspan=10, sticky=EW)
        self.center_frame.grid(row=2, column=0, columnspan=10, sticky=EW)
        self.footer_frame.grid(row=3, column=0, columnspan=10, sticky=EW)

        # Labels
        self.label_footer.grid(row=0, column=0, sticky=EW)

        # Tree Views
        self.tree_person.grid(row=3, column=0, columnspan=10, sticky=EW)
        self.tree_relationships.grid(row=0, column=0, columnspan=10, sticky=NSEW)
        self.tree_phone_numbers.grid(row=0, column=2, sticky=NSEW, columnspan=10)
        self.tree_email.grid(row=3, column=2, sticky=NSEW, columnspan=10)
        self.tree_addresses.grid(row=0, column=1, sticky=NSEW)
        self.tree_identities.grid(row=0, column=1, sticky=NSEW)

        # Search Labels
        self.search_inputs.search_option_menu.grid(row=1, column=0)
        self.search_inputs.radio_contains.grid(row=1, column=1)
        self.search_inputs.radio_equals.grid(row=1, column=2)

        self.search_inputs.entry_search_box.grid(row=1, column=3, sticky=EW)
        self.search_inputs.search_button.grid(row=1, column=4, sticky=EW)

        # Build additional controls
        self.build_person_tree()
        self.build_relationship_tree()
        self.build_phone_tree()
        self.build_email_tree()
        self.build_address_tree()
        self.build_identity_tree()
        self.build_notebook_tabs()

        # Add bottom save button
        self.button_save_changes.grid(row=10, column=1, sticky=EW)

        # Add person buttons
        self.button_edit_phone.grid(row=2, column=2, sticky=W)
        self.button_delete_phone.grid(row=2, column=11, sticky=E)
        self.button_edit_email.grid(row=4, column=2, sticky=W)
        self.button_delete_email.grid(row=4, column=11, sticky=E)
        self.button_delete_person.grid(row=6, column=1, sticky=W)

        # Add relationship buttons
        self.button_delete_relation.grid(row=1, column=0, sticky=W)

        # Add address buttons
        self.button_delete_address.grid(row=1, column=1, sticky=W)

        # Add identification buttons
        self.button_delete_identification.grid(row=1, column=1, sticky=W)

    def build_person_tree(self):

        self.tree_person.heading("firstname", text="First Name", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "firstname", 0))
        self.tree_person.heading("lastname", text="Last Name", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "lastname", 0))
        self.tree_person.heading("middleinitial", text="Middle Ini.", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "middleinitial", 0))
        self.tree_person.heading("nickname", text="NickName", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "nickname", 0))
        self.tree_person.heading("dateofbirth", text="Date of Birth", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "dateofbirth", 0))
        self.tree_person.heading("dateofdeath", text="Date of Death", anchor=W,
                                 command=lambda: sort_by_column(self.tree_person, "dateofdeath", 0))
        self.tree_person.bind('<<TreeviewSelect>>', self.person_row_selected)
        self.tree_person.column("firstname", width=75, anchor=W)
        self.tree_person.column("lastname", width=75, anchor=W)
        self.tree_person.column("middleinitial", width=75, anchor=W)
        self.tree_person.column("nickname", width=75, anchor=W)
        self.tree_person.column("dateofbirth", width=75, anchor=W)
        self.tree_person.column("dateofdeath", width=75, anchor=W)
        # The "show" attribute hides the left most column of tree view which we don't need in this use-case.
        self.tree_person["show"] = "headings"
        # self.tree_person["displaycolumns"] = [4, 8, 9, 18]

        # for col in self.tree_person   .tree_columns:
        #     self.tree.heading(col, text=col.title(),
        #                       command=lambda c=col: self.sortby(self.tree_person, c, 0))


        # TODO: Fix this... it should not be called here maybe elsewhere? Y?N?
        self.fill_tree_person()

    def build_relationship_tree(self):

        self.tree_relationships.heading("firstname", text="First Name", anchor=W,
                                        command=lambda: sort_by_column(self.tree_relationships, "firstname", 0))
        self.tree_relationships.heading("lastname", text="Last Name", anchor=W,
                                        command=lambda: sort_by_column(self.tree_relationships, "lastname", 0))
        self.tree_relationships.heading("middleinitial", text="Middle Ini.", anchor=W,
                                        command=lambda: sort_by_column(self.tree_relationships, "middleinitial", 0))
        self.tree_relationships.heading("typedescription", text="Relation Type", anchor=W,
                                        command=lambda: sort_by_column(self.tree_relationships, "typedescription", 0))

        self.tree_relationships.bind('<<TreeviewSelect>>', self.relationship_row_selected)
        self.tree_relationships.column("firstname", width=175, anchor=W)
        self.tree_relationships.column("lastname", width=175, anchor=W)
        self.tree_relationships.column("middleinitial", width=100, anchor=W)
        self.tree_relationships.column("typedescription", width=280, anchor=W)
        self.tree_relationships["show"] = "headings"

    def build_phone_tree(self):
        self.tree_phone_numbers.heading("personid", text="PID", anchor=W)
        self.tree_phone_numbers.heading("contactid", text="CID", anchor=W)
        self.tree_phone_numbers.heading("phonenumber", text="Phone Number", anchor=W)
        self.tree_phone_numbers.heading("sequenceno", text="Sequence", anchor=W)
        self.tree_phone_numbers.heading("typecode", text="Type Code", anchor=W)
        self.tree_phone_numbers.heading("typedescription", text="Description", anchor=W)
        self.tree_phone_numbers.heading("typeid", text="TypeId", anchor=W)
        self.tree_phone_numbers.bind('<<TreeviewSelect>>', self.tree_phone_row_selected)
        self.tree_phone_numbers.column("personid", width=200, anchor=W)
        self.tree_phone_numbers.column("contactid", width=200, anchor=W)
        self.tree_phone_numbers.column("phonenumber", width=205, anchor=W)
        self.tree_phone_numbers.column("sequenceno", width=80, anchor=W)
        self.tree_phone_numbers.column("typecode", width=90, anchor=W)
        self.tree_phone_numbers.column("typedescription", width=163, anchor=W)
        self.tree_phone_numbers.column("typeid", width=163, anchor=W)
        self.tree_phone_numbers["displaycolumns"] = [2, 3, 5]
        self.tree_phone_numbers["show"] = "headings"

    def build_email_tree(self):
        self.tree_email.heading("personid", text="PID", anchor=W)
        self.tree_email.heading("contactid", text="CID", anchor=W)
        self.tree_email.heading("emailaddress", text="Email", anchor=W)
        self.tree_email.heading("sequenceno", text="Sequence", anchor=W)
        self.tree_email.heading("typeid", text="Type Id", anchor=W)
        self.tree_email.heading("typecode", text="Type", anchor=W)
        self.tree_email.heading("typedescription", text="Description", anchor=W)
        self.tree_email.bind('<<TreeviewSelect>>', self.tree_email_row_selected)
        self.tree_email.column("personid", width=200, anchor=W)
        self.tree_email.column("contactid", width=200, anchor=W)
        self.tree_email.column("emailaddress", width=205, anchor=W)
        self.tree_email.column("sequenceno", width=80, anchor=W)
        self.tree_email.column("typeid", width=90, anchor=W)
        self.tree_email.column("typecode", width=90, anchor=W)
        self.tree_email.column("typedescription", width=163, anchor=W)
        self.tree_email["displaycolumns"] = [2, 3, 6]
        self.tree_email["show"] = "headings"

    def build_address_tree(self):

        self.tree_addresses.heading("addressline1", text="Line 1", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "addressline1", 0))
        self.tree_addresses.heading("addressline2", text="Line 2", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "addressline2", 0))
        self.tree_addresses.heading("pobox", text="PO Box", anchor=W)
        self.tree_addresses.heading("city", text="City", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "city", 0))
        self.tree_addresses.heading("state", text="State", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "state", 0))
        self.tree_addresses.heading("zipcode", text="Zip", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "zipcode", 0))
        self.tree_addresses.heading("zip4", text="Zip4", anchor=W)
        self.tree_addresses.heading("postalcode", text="Postal Code", anchor=W)
        self.tree_addresses.heading("status", text="Status", anchor=W)
        self.tree_addresses.heading("typeid", text="Type Id", anchor=W)
        self.tree_addresses.heading("sequenceno", text="Seq.", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "sequenceno", 0))
        self.tree_addresses.heading("typecode", text="Type Code", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "typecode", 0))
        self.tree_addresses.heading("typedescription", text="Description", anchor=W,
                                    command=lambda: sort_by_column(self.tree_addresses, "typedescription", 0))

        self.tree_addresses.bind('<<TreeviewSelect>>', self.address_row_selected)
        self.tree_addresses.column("addressline1", width=150, anchor=W)
        self.tree_addresses.column("addressline2", width=85, anchor=W)
        self.tree_addresses.column("pobox", width=75, anchor=W)
        self.tree_addresses.column("city", width=85, anchor=W)
        self.tree_addresses.column("state", width=50, anchor=W)
        self.tree_addresses.column("zipcode", width=65, anchor=W)
        self.tree_addresses.column("zip4", width=85, anchor=W)
        self.tree_addresses.column("postalcode", width=85, anchor=W)
        self.tree_addresses.column("status", width=85, anchor=W)
        self.tree_addresses.column("typeid", width=85, anchor=W)
        self.tree_addresses.column("sequenceno", width=35, anchor=W)
        self.tree_addresses.column("typecode", width=85, anchor=W)
        self.tree_addresses.column("typedescription", width=150, anchor=W)
        self.tree_addresses["show"] = "headings"
        self.tree_addresses["displaycolumns"] = [0, 4, 5, 10, 12]

    def build_identity_tree(self):
        self.tree_identities.heading("identificationnumber", text="ID Number", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "identificationnumber", 0))
        self.tree_identities.heading("identificationtypeid", text="Type Id.", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "identificationtypeid", 0))
        self.tree_identities.heading("issuingauthority", text="Authority", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "issuingauthority", 0))
        self.tree_identities.heading("issuingentity", text="Entity", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "issuingentity", 0))
        self.tree_identities.heading("recordlocation", text="Location", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "recordlocation", 0))
        self.tree_identities.heading("typecode", text="Type Code", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "typecode", 0))
        self.tree_identities.heading("typedescription", text="Description", anchor=W,
                                     command=lambda: sort_by_column(self.tree_identities, "typedescription", 0))

        self.tree_identities.bind('<<TreeviewSelect>>', self.identity_row_selected)
        self.tree_identities.column("identificationnumber", width=160, anchor=W)
        self.tree_identities.column("identificationtypeid", width=85, anchor=W)
        self.tree_identities.column("issuingauthority", width=110, anchor=W)
        self.tree_identities.column("issuingentity", width=50, anchor=W)
        self.tree_identities.column("recordlocation", width=25, anchor=W)
        self.tree_identities.column("typecode", width=25, anchor=W)
        self.tree_identities.column("typedescription", width=175, anchor=W)
        self.tree_identities["show"] = "headings"
        self.tree_identities["displaycolumns"] = [0, 2, 6]

    def build_notebook_tabs(self):
        # Position tab frames
        self.person_tab_frame.grid(row=0, column=0)
        self.address_tab_frame.grid(row=0, column=0)
        self.identification_tab_frame.grid(row=0, column=0)
        self.relationship_tab_frame.grid(row=0, column=0)
        self.comments_tab_frame.grid(row=0, column=0, sticky=EW)

        # Add frames to tabs
        self.notebook.add(self.person_tab_frame)
        self.notebook.add(self.address_tab_frame)
        self.notebook.add(self.identification_tab_frame)
        self.notebook.add(self.relationship_tab_frame)
        self.notebook.add(self.comments_tab_frame)

        # Set the order of the tabs and set tab text
        self.notebook.tab(0, text="Person")
        self.notebook.tab(1, text="Address")
        self.notebook.tab(2, text="Identification")
        self.notebook.tab(3, text="Relationships")
        self.notebook.tab(4, text="Comments")
        self.notebook.grid(row=0, column=0, sticky=NSEW, columnspan=10)

        # Next add controls to the tabs
        self.add_notebook_tab_controls()

    def add_notebook_tab_controls(self):
        # Person Labels
        # configure width
        self.person_labels.label_first_name.config(width=13)  # Only one width needed due to sticky
        #   Set in Grid
        self.person_labels.label_first_name.grid(row=0, column=0, sticky=NW)
        self.person_labels.label_last_name.grid(row=1, column=0, sticky=NW)
        self.person_labels.label_middle_initial.grid(row=2, column=0, sticky=NW)
        self.person_labels.label_nick_name.grid(row=3, column=0, sticky=NW)
        self.person_labels.label_date_of_birth.grid(row=4, column=0, sticky=NW)
        self.person_labels.label_date_of_death.grid(row=5, column=0, sticky=NW)

        # Person Inputs
        # configure widths
        self.person_inputs.entry_first_name.config(width=20)
        self.person_inputs.entry_last_name.config(width=20)
        self.person_inputs.entry_middle_initial.config(width=20)
        self.person_inputs.entry_nick_name.config(width=20)
        self.person_inputs.entry_date_of_birth.config(width=20)
        self.person_inputs.entry_date_of_death.config(width=20)
        # Set in Grid
        self.person_inputs.entry_first_name.grid(row=0, column=1, sticky=NW)
        self.person_inputs.entry_last_name.grid(row=1, column=1, sticky=NW)
        self.person_inputs.entry_middle_initial.grid(row=2, column=1, sticky=NW)
        self.person_inputs.entry_nick_name.grid(row=3, column=1, sticky=NW)
        self.person_inputs.entry_date_of_birth.grid(row=4, column=1, sticky=NW)
        self.person_inputs.entry_date_of_death.grid(row=5, column=1, sticky=NW)
        self.person_field_frame.grid(row=0, column=0)

        # Address Labels
        # configure widths
        self.address_labels.label_address_line_1.config(width=13)
        # Set in Grid
        self.address_labels.label_address_line_1.grid(row=0, column=0, sticky=EW)
        self.address_labels.label_address_line_2.grid(row=1, column=0, sticky=EW)
        self.address_labels.label_po_box.grid(row=2, column=0, sticky=EW)
        self.address_labels.label_city.grid(row=3, column=0, sticky=EW)
        self.address_labels.label_state.grid(row=4, column=0, sticky=EW)
        self.address_labels.label_zip_code.grid(row=5, column=0, sticky=EW)
        self.address_labels.label_zip_4.grid(row=6, column=0, sticky=EW)
        self.address_labels.label_postal_code.grid(row=7, column=0, sticky=EW)
        self.address_labels.label_status.grid(row=8, column=0, sticky=EW)
        self.address_labels.label_address_type_id.grid(row=9, column=0, sticky=EW)
        self.address_labels.label_sequence_number.grid(row=10, column=0, sticky=EW)

        # Address Inputs
        # Set in Grid
        self.address_inputs.entry_address_line_1.grid(row=0, column=1, sticky=EW)
        self.address_inputs.entry_address_line_2.grid(row=1, column=1, sticky=EW)
        self.address_inputs.entry_po_box.grid(row=2, column=1, sticky=EW)
        self.address_inputs.entry_city.grid(row=3, column=1, sticky=EW)
        self.address_inputs.entry_state.grid(row=4, column=1, sticky=EW)
        self.address_inputs.entry_zip_code.grid(row=5, column=1, sticky=EW)
        self.address_inputs.entry_zip_4.grid(row=6, column=1, sticky=EW)
        self.address_inputs.entry_postal_code.grid(row=7, column=1, sticky=EW)
        self.address_inputs.entry_status.grid(row=8, column=1, sticky=EW)
        # self.address_inputs.entry_address_type_id.grid(row=8, column=1, sticky=EW)
        self.address_type_options.grid(row=9, column=1, sticky=EW)
        self.address_inputs.entry_sequence_number.grid(row=10, column=1, sticky=EW)
        self.address_type_options.config(width=15)
        self.address_field_frame.grid(row=0, column=0)

        # Identity Labels
        # configure widths
        self.identity_labels.label_identification_id.config(width=13)
        # Set in Grid
        self.identity_labels.label_identification_number.grid(row=1, column=0, sticky=EW)
        self.identity_labels.label_issuing_authority.grid(row=3, column=0, sticky=EW)
        self.identity_labels.label_issuing_entity.grid(row=4, column=0, sticky=EW)
        self.identity_labels.label_record_location.grid(row=5, column=0, sticky=EW)
        self.identity_labels.label_type_code.grid(row=7, column=0, sticky=EW)

        # Identity Inputs
        # Set in Grid
        self.identity_inputs.entry_identification_number.grid(row=1, column=1, sticky=EW)
        self.identity_inputs.entry_issuing_authority.grid(row=3, column=1, sticky=EW)
        self.identity_inputs.entry_issuing_entity.grid(row=4, column=1, sticky=EW)
        self.identity_inputs.entry_record_location.grid(row=5, column=1, sticky=EW)
        self.identity_type_options.grid(row=7, column=1, sticky=EW)
        self.identity_type_options.config(width=15)

        self.identity_field_frame.grid(row=0, column=0)

        # Comment Inputs
        # Comment scroll bar
        self.comments_scroll_bar.config(command=self.comment_inputs.text_comment.yview)
        self.comment_inputs.text_comment.config(width=101, height=22, yscrollcommand=self.comments_scroll_bar.set)

        # Set in Grid
        self.comment_inputs.text_comment.grid(row=2, column=1, sticky=EW)
        self.comments_scroll_bar.grid(row=2, column=2, sticky=NSEW)

        # People scroll bar
        self.person_scroll_bar.config(command=self.tree_person.yview)
        self.person_scroll_bar.grid(row=3, column=12, sticky=NSEW)
        self.tree_person.config(yscrollcommand=self.person_scroll_bar.set)

        # Address scroll bar
        self.address_scroll_bar.config(command=self.tree_addresses.yview)
        self.address_scroll_bar.grid(row=0, column=2, sticky=NSEW)
        self.tree_addresses.config(yscrollcommand=self.address_scroll_bar.set)

        # Phone scroll bar
        self.phone_scroll_bar.config(command=self.tree_phone_numbers.yview)
        self.phone_scroll_bar.grid(row=0, column=12, sticky=NSEW)
        self.tree_phone_numbers.config(yscrollcommand=self.phone_scroll_bar.set)

        # Email scroll bar
        self.email_scroll_bar.config(command=self.tree_email.yview)
        self.email_scroll_bar.grid(row=3, column=12, sticky=NSEW)
        self.tree_email.config(yscrollcommand=self.email_scroll_bar.set)

        # Identity scroll bar
        self.identities_scroll_bar.config(command=self.tree_identities.yview)
        self.identities_scroll_bar.grid(row=0, column=12, sticky=NSEW)
        self.tree_identities.config(yscrollcommand=self.identities_scroll_bar.set)

        # Relationship scroll bar
        self.relationship_scroll_bar.config(command=self.tree_relationships.yview)
        self.relationship_scroll_bar.grid(row=0, column=12, sticky=NSEW)
        self.tree_relationships.config(yscrollcommand=self.relationship_scroll_bar.set)

    def open_about_ui(self):
        aui = about_ui.AboutUi(Toplevel(), self)
        aui.apply_layout()
        pass

    def open_help_ui(self):
        hui = help_ui.HelpUi(Toplevel(), self)
        hui.apply_layout()
        pass

    def open_person_ui(self, mode):
        pui = person_ui.PersonUi(Toplevel(), mode, self)
        pui.apply_layout()

    def open_address_ui(self):
        if self.tree_person_row_iid is not None:
            address = address_ui.AddressUi(Toplevel(), "insert", self)
            address.person_id = self.tree_person_row_iid
            address.apply_layout()

    def open_relation_ui(self):
        if self.tree_person_row_iid is not None:
            row_item = self.tree_person.item(self.tree_person_row_iid)
            row_values = row_item['values']
            name_title = ("Assigning relationship to: ", str(row_values[0]), " ", str(row_values[1]))
            self.relationship_child_top_level = Toplevel()
            self.relationship_child_top_level.wm_title("".join(name_title))
            relation = relation_ui.RelationUi(self.relationship_child_top_level, "insert", self)
            relation.person_id = self.tree_person_row_iid
            relation.apply_layout()

    def open_phone_ui(self, record_event_type):
        if self.tree_person_row_iid is not None:
            if record_event_type == CreateRecord.phone:
                contact_phone_ui = phone_ui.PhoneUi(Toplevel(), "insert", self)
                contact_phone_ui.person_id = self.tree_person_row_iid
                contact_phone_ui.apply_layout()
            elif record_event_type == EditRecord.phone:
                if self.tree_phone_row_iid is not None:
                    contact_phone_ui = phone_ui.PhoneUi(Toplevel(), "update", self)
                    contact_phone_ui.person_id = self.selected_phone_record.person_id
                    contact_phone_ui.inputs.variable_contact_id.set(self.selected_phone_record.contact_id)
                    contact_phone_ui.inputs.variable_sequence_number.set(self.selected_phone_record.sequence_number)
                    contact_phone_ui.inputs.variable_area_code.set(self.selected_phone_record.area_code)
                    contact_phone_ui.inputs.variable_exchange.set(self.selected_phone_record.exchange)
                    contact_phone_ui.inputs.variable_trunk.set(self.selected_phone_record.trunk)
                    contact_phone_ui.inputs.variable_phone_type.set(self.selected_phone_record.type_code)
                    contact_phone_ui.apply_layout()

    def open_email_ui(self, record_event_type):
        if self.tree_person_row_iid is not None:
            if record_event_type == CreateRecord.email:
                contact_email_ui = email_ui.EmailUi(Toplevel(), "insert", self)
                contact_email_ui.person_id = self.tree_person_row_iid
                contact_email_ui.apply_layout()
            elif record_event_type == EditRecord.email:
                if self.tree_email_row_iid is not None:
                    contact_email_ui = email_ui.EmailUi(Toplevel(), "update", self)
                    contact_email_ui.person_id = self.selected_email_record.person_id
                    contact_email_ui.inputs.variable_contact_id.set(self.selected_email_record.contact_id)
                    contact_email_ui.inputs.variable_email_address.set(self.selected_email_record.email_address)
                    contact_email_ui.inputs.variable_email_type.set(self.selected_email_record.type_code)
                    contact_email_ui.inputs.variable_sequence_number.set(self.selected_email_record.sequence_number)
                    contact_email_ui.apply_layout()

    def open_identity_ui(self):
        if self.tree_person_row_iid is not None:
            identity = identity_ui.IdentityUi(Toplevel(), "insert", self)
            identity.person_id = self.tree_person_row_iid
            identity.apply_layout()

    def person_row_selected(self, event):
        # Clear previous tree selected rows.
        self.tree_person_row_iid = self.tree_person.focus()
        row_item = self.tree_person.item(self.tree_person_row_iid)
        row_values = row_item['values']

        self.fill_tree_relationships(self.tree_person_row_iid)
        self.fill_tree_addresses(self.tree_person_row_iid)
        self.fill_tree_identities(self.tree_person_row_iid)
        self.fill_tree_phone_numbers(self.tree_person_row_iid)
        self.fill_tree_email(self.tree_person_row_iid)
        self.fill_comment(self.tree_person_row_iid)

        # SET person fields with the selected row values
        self.person_inputs.variable_first_name.set(row_values[0])
        self.person_inputs.variable_last_name.set(row_values[1])
        self.person_inputs.variable_middle_initial.set(row_values[2])
        self.person_inputs.variable_nick_name.set(row_values[3])
        self.person_inputs.variable_date_of_birth.set(row_values[4])
        self.person_inputs.variable_date_of_death.set(row_values[5])

    def address_row_selected(self, event):
        self.tree_address_row_iid = self.tree_addresses.focus()
        row_item = self.tree_addresses.item(self.tree_address_row_iid)
        row_values = row_item['values']

        # SET address fields with the selected row values
        self.address_inputs.variable_address_line_1.set(row_values[0])
        self.address_inputs.variable_address_line_2.set(row_values[1])
        self.address_inputs.variable_po_box.set(row_values[2])
        self.address_inputs.variable_city.set(row_values[3])
        self.address_inputs.variable_state.set(row_values[4])
        self.address_inputs.variable_zip_code.set(row_values[5])
        self.address_inputs.variable_zip_4.set(row_values[6])
        self.address_inputs.variable_postal_code.set(row_values[7])
        self.address_inputs.variable_status.set(row_values[8])
        self.address_inputs.variable_address_type_id.set(row_values[9])
        self.address_inputs.variable_sequence_number.set(row_values[10])
        self.address_inputs.variable_type_code.set(row_values[11])
        self.address_inputs.variable_type_description.set(row_values[12])
        for c in self.address_codes:
            if c.type_description == self.address_inputs.variable_type_description.get():
                self.address_inputs.variable_address_type_id.set(c.type_id)
                self.address_type_option_variable.set(self.address_inputs.variable_type_description.get())

    def identity_row_selected(self, event):
        self.tree_identity_row_iid = self.tree_identities.focus()
        row_item = self.tree_identities.item(self.tree_identity_row_iid)
        row_values = row_item['values']
        # SET address fields with the selected row values
        self.identity_inputs.variable_identification_number.set(row_values[0])
        self.identity_inputs.variable_issuing_authority.set(row_values[2])
        self.identity_inputs.variable_issuing_entity.set(row_values[3])
        self.identity_inputs.variable_record_location.set(row_values[4])
        # self.identity_inputs.variable_identification_id.set(row_values[5])
        self.identity_inputs.variable_type_code.set(row_values[5])
        self.identity_inputs.variable_type_description.set(row_values[6])
        for c in self.identity_codes:
            if c.type_description == self.identity_inputs.variable_type_description.get():
                self.identity_inputs.variable_type_code.set(c.type_id)
                self.identity_type_option_variable.set(self.identity_inputs.variable_type_description.get())

    def relationship_row_selected(self, event):
        self.tree_relationship_row_iid = self.tree_relationships.focus()

    def tree_phone_row_selected(self, event):
        self.tree_phone_row_iid = self.tree_phone_numbers.focus()
        row_item = self.tree_phone_numbers.item(self.tree_phone_row_iid)
        row_values = row_item['values']
        self.selected_phone_record.person_id = self.tree_person_row_iid
        self.selected_phone_record.contact_id = row_values[1]
        phone_number = row_values[2].split(" ")
        self.selected_phone_record.area_code = phone_number[0]
        self.selected_phone_record.exchange = phone_number[1]
        self.selected_phone_record.trunk = phone_number[2]
        self.selected_phone_record.sequence_number = row_values[3]
        self.selected_phone_record.type_code = row_values[6]

    def tree_email_row_selected(self, event):
        self.tree_email_row_iid = self.tree_email.focus()
        row_item = self.tree_email.item(self.tree_email_row_iid)
        row_values = row_item['values']
        self.selected_email_record.person_id = self.tree_person_row_iid  # 0
        self.selected_email_record.contact_id = row_values[1]
        self.selected_email_record.email_address = row_values[2]
        self.selected_email_record.sequence_number = row_values[3]
        self.selected_email_record.type_code = row_values[4]

    def fill_tree_person(self):
        for row in self.tree_person.get_children():
            self.tree_person.delete(row)

        for person in read_people():
            self.tree_person.insert("", "end", iid=person.person_id,
                                    values=[person.first_name, person.last_name, person.middle_initial,
                                            person.nick_name, person.date_of_birth,
                                            person.date_of_death])

    def fill_tree_relationships(self, row_iid):
        relatives = read_relationships(row_iid)

        # delete existing rows before inserting new ones
        for row in self.tree_relationships.get_children():
            self.tree_relationships.delete(row)

        for relation in relatives:
            self.tree_relationships.insert("", relation.relationship_id, relation.relationship_id,
                                           values=[
                                              relation.person.first_name, relation.person.last_name,
                                              relation.person.middle_initial, relation.relationship_type_description])

    def fill_tree_addresses(self, row_iid):
        addresses = read_addresses(row_iid)
        # delete existing rows before inserting new ones
        for row in self.tree_addresses.get_children():
            self.tree_addresses.delete(row)

        # Clear the address fields before filling them
        self.clear_address_inputs()

        # get the first address in the sequence to display as default
        # but only if we have at least one address
        # because we are using a class object in a list we must pass
        # an attribute key name so we can compare each class object in the list
        # RULE: When the person selected changes, get the addresses, but display and select the first in the series.
        if len(addresses) > 0:
            first_address = min(addresses, key=attrgetter("sequence_number"))
            self.address_inputs.variable_address_line_1.set(first_address.address_line_1)
            self.address_inputs.variable_address_line_2.set(first_address.address_line_2)
            self.address_inputs.variable_po_box.set(first_address.po_box)
            self.address_inputs.variable_city.set(first_address.city)
            self.address_inputs.variable_state.set(first_address.state)
            self.address_inputs.variable_zip_code.set(first_address.zip_code)
            self.address_inputs.variable_zip_4.set(first_address.zip4)
            self.address_inputs.variable_postal_code.set(first_address.postal_code)
            self.address_inputs.variable_status.set(first_address.status)
            self.address_inputs.variable_address_type_id.set(first_address.type_id)
            self.address_inputs.variable_sequence_number.set(first_address.sequence_number)
            self.address_inputs.variable_type_code.set(first_address.type_description)

            for address in addresses:
                self.tree_addresses.insert("", address.address_id, address.address_id,
                                           values=[address.address_line_1, address.address_line_2, address.po_box,
                                                   address.city, address.state, address.zip_code, address.zip4,
                                                   address.postal_code, address.status, address.type_id,
                                                   address.sequence_number, address.type_code,
                                                   address.type_description])

            # Set the default selected row to the first in the series
            for row in self.tree_addresses.get_children():
                if row == str(first_address.address_id):
                    self.tree_addresses.focus_set()
                    self.tree_addresses.selection_set((row, row))
                    self.tree_addresses.focus(row)
        if len(addresses) == 0:
            self.address_type_option_variable.set("PLEASE-SELECT")

    def fill_tree_identities(self, row_iid):
        identities = read_identification(row_iid)
        # delete existing rows before inserting new ones
        for row in self.tree_identities.get_children():
            self.tree_identities.delete(row)

        # Clear identity inputs before filling
        self.clear_identity_inputs()

        if len(identities) > 0:
            first_identification = min(identities, key=attrgetter("identification_id"))
            self.identity_inputs.variable_person_id.set(first_identification.person_id)
            self.identity_inputs.variable_identification_number.set(first_identification.identification_number)
            self.identity_inputs.variable_issuing_authority.set(first_identification.issuing_authority)
            self.identity_inputs.variable_issuing_entity.set(first_identification.issuing_entity)
            self.identity_inputs.variable_record_location.set(first_identification.record_location)
            self.identity_inputs.variable_identification_id.set(first_identification.identification_id)
            self.identity_inputs.variable_type_code.set(first_identification.type_code)
            self.identity_inputs.variable_type_description.set(first_identification.type_description)

            for identity in identities:
                self.tree_identities.insert("", identity.identification_id, identity.identification_id,
                                            values=[identity.identification_number, identity.identification_type_id,
                                                    identity.issuing_authority, identity.issuing_entity,
                                                    identity.record_location,
                                                    identity.type_code, identity.type_description])

            # Set the default selected row to the first in the series
            for row in self.tree_identities.get_children():
                if row == str(first_identification.identification_id):
                    self.tree_identities.focus_set()
                    self.tree_identities.selection_set((row, row))
                    self.tree_identities.focus(row)
        if len(identities) == 0:
            self.identity_type_option_variable.set("PLEASE-SELECT")

    def fill_tree_phone_numbers(self, row_iid):
        # Set None here to clear out previous selection
        self.tree_phone_row_iid = None

        # Get data from the database
        phone_numbers = read_phone_contacts(row_iid)

        # Delete existing rows before inserting new ones
        for row in self.tree_phone_numbers.get_children():
            self.tree_phone_numbers.delete(row)

        for phone in phone_numbers:
            self.tree_phone_numbers.insert("", phone.contact_id, phone.contact_id,
                                           values=[phone.person_id, phone.contact_id,
                                                   (phone.area_code, phone.exchange, phone.trunk),
                                                   phone.sequence_number, phone.type_code,
                                                   phone.type_description, phone.phone_type_id])

        # Get the first in the sequence as we assume that the first
        # Rule: Assume first in the sequence is most important so select it if it exists.
        if len(phone_numbers) > 0:
            first_phone = min(phone_numbers, key=attrgetter("sequence_number"))
            # Set the default selected row to the first in the series
            for row in self.tree_phone_numbers.get_children():
                if row == str(first_phone.contact_id):
                    # self.tree_phone_numbers.focus_set()
                    self.tree_phone_numbers.selection_set((row, row))
                    self.tree_phone_numbers.focus(row)

    def fill_tree_email(self, row_iid):
        self.tree_email_row_iid = None
        email_addresses = read_email_contacts(row_iid)
        # delete existing rows before inserting new ones
        for row in self.tree_email.get_children():
            self.tree_email.delete(row)

        for email in email_addresses:
            self.tree_email.insert("", email.contact_id, email.contact_id,
                                   values=[email.person_id, email.contact_id, email.email_address,
                                           email.sequence_number, email.email_type_id, email.type_code,
                                           email.type_description])

        # Get the first in the sequence as we assume that the first
        # Rule: Assume first in the sequence is most important so select it if it exists.
        if len(email_addresses) > 0:
            first_email = min(email_addresses, key=attrgetter("sequence_number"))
            # Set the default selected row to the first in the series
            for row in self.tree_email.get_children():
                if row == str(first_email.contact_id):
                    # self.tree_email.focus_set()
                    self.tree_email.selection_set((row, row))
                    self.tree_email.focus(row)

    def fill_comment(self, row_iid):
        comments = read_comment(row_iid)
        self.clear_comments()
        # fill comment widgets with values
        for comment in comments:
            self.comment_inputs.variable_comment_id.set(comment.comment_id)
            self.comment_inputs.variable_person_id.set(comment.person_id)
            self.comment_inputs.text_comment.insert('1.0', comment.comment)

    def clear_comments(self):
        # clear existing comment
        self.comment_inputs.variable_comment_id.set("")
        self.comment_inputs.variable_person_id.set("")
        self.comment_inputs.text_comment.delete('1.0', END)

    def clear_address_inputs(self):
        self.tree_address_row_iid = None
        self.address_inputs.variable_address_line_1.set("")
        self.address_inputs.variable_address_line_2.set("")
        self.address_inputs.variable_po_box.set("")
        self.address_inputs.variable_city.set("")
        self.address_inputs.variable_state.set("")
        self.address_inputs.variable_zip_code.set("")
        self.address_inputs.variable_zip_4.set("")
        self.address_inputs.variable_postal_code.set("")
        self.address_inputs.variable_status.set("")
        self.address_inputs.variable_address_type_id.set("")
        self.address_inputs.variable_sequence_number.set("")
        self.address_inputs.variable_type_code.set("")
        self.address_inputs.variable_type_description.set("")

    def clear_identity_inputs(self):
        self.tree_identity_row_iid = None
        self.identity_inputs.variable_person_id.set("")
        self.identity_inputs.variable_identification_number.set("")
        self.identity_inputs.variable_issuing_authority.set("")
        self.identity_inputs.variable_issuing_entity.set("")
        self.identity_inputs.variable_record_location.set("")
        self.identity_inputs.variable_identification_id.set("")
        self.identity_inputs.variable_type_code.set("")
        self.identity_inputs.variable_type_description.set("")

    def clear_person_inputs(self):
        self.tree_person_row_iid = None
        self.person_inputs.variable_first_name.set("")
        self.person_inputs.variable_last_name.set("")
        self.person_inputs.variable_middle_initial.set("")
        self.person_inputs.variable_nick_name.set("")
        self.person_inputs.variable_date_of_birth.set("")
        self.person_inputs.variable_date_of_death.set("")

    def clear_all_tab_controls(self):
        self.clear_comments()
        self.clear_address_inputs()
        self.clear_identity_inputs()
        self.clear_person_inputs()

        # Relationship
        for row_relation in self.tree_relationships.get_children():
            self.tree_relationships.delete(row_relation)
        # Addresses
        for row_address in self.tree_addresses.get_children():
            self.tree_addresses.delete(row_address)
        # Identity
        for row_identity in self.tree_identities.get_children():
            self.tree_identities.delete(row_identity)
        # Phone
        for row_phone in self.tree_phone_numbers.get_children():
            self.tree_phone_numbers.delete(row_phone)
        # Email
        for row_email in self.tree_email.get_children():
            self.tree_email.delete(row_email)

    def get_search_results(self):
        # clear control values
        self.clear_all_tab_controls()
        # get search results
        search_option = self.search_inputs.variable_search_option.get()
        search_value = self.search_inputs.variable_search_box.get()
        radio_value = self.search_inputs.variable_radio_option.get()

        if search_option in {"Select Filter", "All"}:
            if search_option == "Select Filter":
                messagebox.showinfo("Search Filter Not Selected", "Please a filter option.")
                return
            search_value = None

        if search_value == "":
            search_value = None

        people = []
        # Search rule: If radio not selected assume "Contains" value as search.
        # search 1: Equals (case insensitive) sql "="
        # search 2: Contains (case insensitive) sql "LIKE %?%"
        if radio_value == 0:
            people = search_people_2(search_option, search_value)
            self.search_inputs.variable_radio_option.set(2)
        if radio_value == 1:
            people = search_people_1(search_option, search_value)
        if radio_value == 2:
            people = search_people_2(search_option, search_value)

        for row in self.tree_person.get_children():
            self.tree_person.delete(row)

        # fill the tree
        for person in people:
            self.tree_person.insert("", "end", iid=person.person_id,
                                    values=[person.first_name, person.last_name, person.middle_initial,
                                            person.nick_name, person.date_of_birth,
                                            person.date_of_death])

    def delete_record(self, record_event_type):
        if not self.tree_person_row_iid:
            return
        selected_row = self.tree_person.selection()
        if selected_row == "":
            return  # Quit here no person row is selected
        if record_event_type == DeleteRecord.person:
            message_content = "Are you sure you want to delete the person?\n\n{0} {1}\n\n{2}"\
                .format(self.person_inputs.variable_first_name.get(),
                        self.person_inputs.variable_last_name.get(),
                        "All data for this person will be deleted and cannot be undone!\n")
            is_yes = messagebox.askyesno("Delete Person?", message_content)
            if is_yes:
                delete_person(self.tree_person_row_iid)
                self.clear_all_tab_controls()
                self.fill_tree_person()
        elif record_event_type == DeleteRecord.address:
            selected_row = self.tree_addresses.selection()
            if selected_row == "":
                return  # Quit here no address is selected
            is_yes = messagebox.askyesno(
                "Delete Address?",
                "Are you sure you want to delete the address?\n\n{0}\n{1}\n{2} {3}".format(
                    self.address_inputs.variable_address_line_1.get(),
                    self.address_inputs.variable_city.get(),
                    self.address_inputs.variable_state.get(),
                    self.address_inputs.variable_zip_code.get()))
            if is_yes:
                delete_address(self.tree_address_row_iid)
                self.fill_tree_addresses(self.tree_person_row_iid)
        elif record_event_type == DeleteRecord.phone:
            selected_row = self.tree_phone_numbers.selection()
            if selected_row == "":
                return  # Quit here no phone row is selected
            is_yes = messagebox.askyesno("Delete Phone Number?",
                                         "Are you sure you want to delete the selected phone number?")
            if is_yes:
                delete_contact(self.tree_phone_row_iid)
                self.fill_tree_phone_numbers(self.tree_person_row_iid)
        elif record_event_type == DeleteRecord.email:
            selected_row = self.tree_email.selection()
            if selected_row == "":
                return  # Quit here no email row is selected
            is_yes = messagebox.askyesno("Delete Email Address?",
                                         "Are you sure you want to delete the selected email address?")
            if is_yes:
                delete_contact(self.tree_email_row_iid)
                self.fill_tree_email(self.tree_person_row_iid)
        elif record_event_type == DeleteRecord.relation:
            selected_row = self.tree_relationships.selection()
            if selected_row == "":
                return  # Quit here because nothing is selected
            is_yes = messagebox.askyesno("Delete Relation?",
                                         "Are you sure you want to delete the selected relationship?")
            if is_yes:
                delete_relationship(self.tree_relationship_row_iid)
                self.fill_tree_relationships(self.tree_person_row_iid)
        elif record_event_type == DeleteRecord.identification:
            selected_row = self.tree_identities.selection()
            if selected_row == "":
                return  # Quit here because nothing is selected
            is_yes = messagebox.askyesno("Delete Identification?",
                                         "Are you sure you want to delete the selected identification?")
            if is_yes:
                delete_identification(self.tree_identity_row_iid)
                self.fill_tree_identities(self.tree_person_row_iid)

    def get_address_codes(self):
        self.address_codes = read_lookup_code_by_reference("address")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in self.address_codes:
            choices.append(code.type_description)
        return choices

    def get_id_codes(self):
        self.identity_codes = read_lookup_code_by_reference("id")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in self.identity_codes:
            choices.append(code.type_description)
        return choices

    def set_identification_type_id(self, event):
        for c in self.identity_codes:
            if c.type_description == self.identity_type_option_variable.get():
                self.identity_inputs.variable_type_code.set(c.type_id)

    def save_dashboard_changes(self):
        row_iid = self.tree_person_row_iid
        if self.save_person() and self.save_address() and self.save_identity() and self.save_comment():
            self.fill_tree_person()
            self.fill_tree_addresses(self.tree_person_row_iid)
            self.fill_tree_identities(self.tree_person_row_iid)

            # Reset the selected row to the row that we just saved.
            self.tree_person.focus(row_iid)
            self.tree_person_row_iid = row_iid
            self.tree_person.selection_set(row_iid)

    def save_person(self):
        if self.tree_person_row_iid is not None:
            if self.validate_person():
                p = Person
                p.person_id = self.tree_person_row_iid
                p.first_name = self.person_inputs.variable_first_name.get()
                p.last_name = self.person_inputs.variable_last_name.get()
                p.middle_initial = self.person_inputs.variable_middle_initial.get()
                p.nick_name = self.person_inputs.variable_nick_name.get()
                p.date_of_birth = self.person_inputs.variable_date_of_birth.get()
                p.date_of_death = self.person_inputs.entry_date_of_death.get()
                if update_person(p):
                    return True
                else:
                    return False

    def save_address(self):
        if self.tree_person_row_iid is not None:
            if self.tree_address_row_iid is not None:
                if self.validate_address():
                    for c in self.address_codes:
                        if c.type_description == self.address_type_option_variable.get():
                            self.address_inputs.variable_address_type_id.set(c.type_id)
                    a = Address
                    a.person_id = self.tree_person_row_iid
                    a.address_id = self.tree_address_row_iid
                    a.address_line_1 = self.address_inputs.variable_address_line_1.get()
                    a.address_line_2 = self.address_inputs.variable_address_line_2.get()
                    a.po_box = self.address_inputs.variable_po_box.get()
                    a.city = self.address_inputs.variable_city.get()
                    a.state = self.address_inputs.variable_state.get()
                    a.zip_code = self.address_inputs.variable_zip_code.get()
                    a.zip4 = self.address_inputs.variable_zip_4.get()
                    a.postal_code = self.address_inputs.variable_postal_code.get()
                    a.status = self.address_inputs.variable_status.get()
                    a.sequence_number = self.address_inputs.variable_sequence_number.get()
                    a.type_id = self.address_inputs.variable_address_type_id.get()
                    # TODO: fix the discrepancy between type_code and type_id ...
                    # All should now be type_id or type_code not both
                    if update_address(a):
                        return True
                    else:
                        return False
            else:
                if len(self.tree_addresses.get_children()) == 0:
                    # If tree iid is None we either don't have an address selected or
                    # there are no addresses in the tree. So, first check if there are any
                    # rows by getting the children. If none, we cannot update address therefore
                    # default to True
                    return True

    def validate_address(self):
        validation_result = False
        line1_is_valid = False
        city_is_valid = False
        state_is_valid = False
        zip_is_valid = False
        sequence_is_valid = False
        address_type_is_valid = False
        # Widgets allow removing of value and for IntVar() assigned to widget tosses a
        # value error when trying to get the value of IntVar() because it contains an empty string.
        # so default to zero and then proceed with validation.
        zip_code = 0
        zip4 = 0
        sequence = 0
        try:
            zip4 = self.address_inputs.variable_zip_4.get()
        except ValueError:
            self.address_inputs.variable_zip_4.set(zip4)
        try:
            zip_code = self.address_inputs.variable_zip_code.get()
        except ValueError:
            self.address_inputs.variable_zip_code.set(zip_code)
        try:
            sequence = self.address_inputs.variable_sequence_number.get()
        except ValueError:
            self.address_inputs.variable_sequence_number.set(sequence)

        try:
            if self.tree_person_row_iid is not None:
                if len(self.address_inputs.variable_address_line_1.get()) > 0:
                    line1_is_valid = True
                if len(self.address_inputs.variable_city.get()) > 0:
                    city_is_valid = True
                if len(self.address_inputs.variable_state.get()) > 0:
                    state_is_valid = True
                if zip_code > 0:
                    zip_is_valid = True
                if sequence > 0:
                    sequence_is_valid = True
                if self.address_inputs.variable_address_type_id.get() > 0:
                    address_type_is_valid = True
                if line1_is_valid and \
                        city_is_valid and \
                        state_is_valid and \
                        zip_is_valid and \
                        address_type_is_valid and \
                        sequence_is_valid:
                    validation_result = True
            error_list = []
            if not sequence_is_valid:
                error_list.append("Sequence must be a number greater than zero.")
            if not address_type_is_valid:
                error_list.append("Address type is invalid.")
            if not zip_is_valid:
                error_list.append("Zip code is not valid.")
            if not state_is_valid:
                error_list.append("State is required.")
            if not city_is_valid:
                error_list.append("City is required.")
            if not line1_is_valid:
                error_list.append("Address line 1 is required.")

            if not validation_result:
                messagebox.showinfo("Address Validation Error", "\n".join(reversed(error_list)))
            return validation_result
        except ValueError:
            validation_result = False
            messagebox.showinfo("Address Validation Error", "Error! Value not valid for input")
            return validation_result

    def validate_person(self):
        # First and last names are required to save. So before save check if provided.
        validation_result = False
        is_first_name_valid = False
        is_last_name_valid = False
        is_date_of_birth_valid = False
        is_date_of_death_valid = False

        error_list = []
        if len(self.person_inputs.variable_first_name.get()) == 0:
            is_first_name_valid = False
            error_list.append("First name is required")
        if len(self.person_inputs.variable_last_name.get()) == 0:
            is_last_name_valid = False
            error_list.append("Last name is required")

        if len(self.person_inputs.variable_first_name.get()) > 0:
            is_first_name_valid = True
        if len(self.person_inputs.variable_last_name.get()) > 0:
            is_last_name_valid = True

        date_of_birth = self.person_inputs.variable_date_of_birth.get()
        date_of_death = self.person_inputs.variable_date_of_death.get()

        # Dates (DOB and DOD) not required but if present must be valid dates.
        # Expected date format is: YYYY-MM-DD
        if len(date_of_birth) > 0:
            try:
                date_value = None
                if len(date_of_birth) > 0:
                    date_value = date_of_birth.split("-")
                datetime.datetime(int(date_value[0]), int(date_value[1]), int(date_value[2]))
                is_date_of_birth_valid = True
            except ValueError:
                error_list.append("Birth Date: Expected YYYY-MM-DD")
                is_date_of_birth_valid = False
            except IndexError:
                error_list.append("Birth Date: Expected YYYY-MM-DD")
                is_date_of_birth_valid = False
            except TypeError:
                error_list.append("Birth Date: Expected YYYY-MM-DD")
                is_date_of_birth_valid = False

        if len(date_of_death) > 0:
            try:
                date_value = None
                if len(date_of_death) > 0:
                    date_value = date_of_death.split("-")
                datetime.datetime(int(date_value[0]), int(date_value[1]), int(date_value[2]))
                is_date_of_death_valid = True
            except ValueError:
                error_list.append("Death Date: Expected YYYY-MM-DD")
                is_date_of_death_valid = False
            except IndexError:
                error_list.append("Death Date: Expected YYYY-MM-DD")
                is_date_of_death_valid = False
            except TypeError:
                error_list.append("Death Date: Expected YYYY-MM-DD")
                is_date_of_death_valid = False

        # Because DOB and DOD is NOT required we set to TRUE here because values, if supplied are validated above.
        if len(date_of_birth) == 0:
            is_date_of_birth_valid = True
        if len(date_of_death) == 0:
            is_date_of_death_valid = True

        if is_first_name_valid and is_last_name_valid and is_date_of_birth_valid and is_date_of_death_valid:
            validation_result = True
        if len(error_list) > 0:
            messagebox.showinfo("Person Validation Error", "\n".join(error_list))
        return validation_result

    def save_identity(self):
        if self.tree_person_row_iid:
            if self.tree_identity_row_iid:
                if self.validate_identification():
                    identification = Identity()
                    identification.person_id = self.tree_person_row_iid
                    identification.type_code = self.identity_inputs.variable_type_code.get()
                    identification.identification_number = self.identity_inputs.variable_identification_number.get()
                    identification.issuing_authority = self.identity_inputs.variable_issuing_authority.get()
                    identification.issuing_entity = self.identity_inputs.variable_issuing_entity.get()
                    identification.record_location = self.identity_inputs.variable_record_location.get()
                    identification.identification_id = self.tree_identity_row_iid
                    if update_identification(identification):
                        return True
                    else:
                        return False
            else:
                if len(self.tree_identities.get_children()) == 0:
                    # default to true if no rows are selected or exist
                    return True

    def validate_identification(self):
        valid_type_id = False
        valid_id_number = False
        validation_result = False
        error_list = []
        try:
            if self.tree_person_row_iid is not None:
                if self.identity_inputs.variable_type_code.get() > 0:
                    valid_type_id = True
                if len(self.identity_inputs.variable_identification_number.get()) > 0:
                    valid_id_number = True

                if valid_type_id and valid_id_number:
                    validation_result = True
                if not valid_id_number:
                    error_list.append("Identification number is required")
                if not valid_id_number:
                    error_list.append("Type is invalid")
                if len(error_list) > 0:
                    messagebox.showinfo("Identity Validation Error", "\n".join(error_list))
            return validation_result
        except ValueError:
            validation_result = False
            messagebox.showinfo("Identity Validation Error", "Invalid identity value.")
            return validation_result

    def save_comment(self):
        c = Comment
        # comment_id = 0
        if self.tree_person_row_iid:
            try:
                comment_id = self.comment_inputs.variable_comment_id.get()
            except ValueError:
                comment_id = 0
            if comment_id > 0:
                c.comment_id = comment_id
                c.comment = self.comment_inputs.text_comment.get("1.0", "end-1c")
                c.person_id = self.tree_person_row_iid
                if update_comment(c):
                    return True
                else:
                    return False
            if comment_id == 0:
                c.comment_id = None
                c.comment = self.comment_inputs.text_comment.get("1.0", "end-1c")
                c.person_id = self.tree_person_row_iid
                if create_comment(c):
                    return True
                else:
                    return False
