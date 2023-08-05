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


from tkinter import *
from tkinter.ttk import *

from addressbook.ui.rules import InputValidation

# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/entry-validation.html
# edit mode ???


class AddressLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_address_line_1 = Label(self.container_widget, padding=2, text="Address Line 1")
        self.label_address_line_2 = Label(self.container_widget, padding=2, text="Address Line 2")
        self.label_po_box = Label(self.container_widget, padding=2, text="PO Box")
        self.label_city = Label(self.container_widget, padding=2, text="City")
        self.label_state = Label(self.container_widget, padding=2, text="State")
        self.label_zip_code = Label(self.container_widget, padding=2, text="Zip Code")
        self.label_zip_4 = Label(self.container_widget, padding=2, text="Zip-4")
        self.label_postal_code = Label(self.container_widget, padding=2, text="Postal Code")
        self.label_status = Label(self.container_widget, padding=2, text="Status")
        self.label_address_type_id = Label(self.container_widget, padding=2, text="Type")
        self.label_sequence_number = Label(self.container_widget, padding=2, text="Sequence No.")
        self.label_address_type_code = Label(self.container_widget, padding=2, text="Type Code")
        self.label_address_type_description = Label(self.container_widget, padding=2, text="Description")


class AddressInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)
        self.variable_address_line_1 = StringVar()
        self.variable_address_line_2 = StringVar()
        self.variable_po_box = StringVar()
        self.variable_city = StringVar()
        self.variable_state = StringVar()
        self.variable_zip_code = IntVar()
        self.variable_zip_4 = IntVar()
        self.variable_postal_code = StringVar()
        self.variable_status = StringVar()
        self.variable_address_type_id = IntVar()
        self.variable_sequence_number = IntVar()
        self.variable_type_code = StringVar()
        self.variable_type_description = StringVar()
        self.input_rules.set_address_validation_commands()

        self.entry_address_line_1 = Entry(self.container_widget,
                                          textvariable=self.variable_address_line_1,
                                          validate="key",
                                          validatecommand=self.input_rules.validate_address_line_1)

        self.entry_address_line_2 = Entry(self.container_widget,
                                          textvariable=self.variable_address_line_2,
                                          validate="key",
                                          validatecommand=self.input_rules.validate_address_line_2)

        self.entry_po_box = Entry(self.container_widget,
                                  textvariable=self.variable_po_box,
                                  validate="key",
                                  validatecommand=self.input_rules.validate_address_pobox)

        self.entry_city = Entry(self.container_widget,
                                textvariable=self.variable_city,
                                validate="key",
                                validatecommand=self.input_rules.validate_address_city)

        self.entry_state = Entry(self.container_widget,
                                 textvariable=self.variable_state,
                                 validate="key",
                                 validatecommand=self.input_rules.validate_address_state)

        self.entry_zip_code = Entry(self.container_widget,
                                    textvariable=self.variable_zip_code,
                                    validate="key",
                                    validatecommand=self.input_rules.validate_address_zip)

        self.entry_zip_4 = Entry(self.container_widget, textvariable=self.variable_zip_4,
                                 validate="key",
                                 validatecommand=self.input_rules.validate_address_zip4)

        self.entry_postal_code = Entry(self.container_widget,
                                       textvariable=self.variable_postal_code,
                                       validate="key",
                                       validatecommand=self.input_rules.validate_address_postal)

        self.entry_status = Entry(self.container_widget,
                                  textvariable=self.variable_status,
                                  validate="key",
                                  validatecommand=self.input_rules.validate_address_status)

        self.entry_address_type_id = Entry(self.container_widget,
                                           textvariable=self.variable_address_type_id,
                                           validate="key",
                                           validatecommand=self.input_rules.validate_address_type_id)

        self.entry_sequence_number = Entry(self.container_widget,
                                           textvariable=self.variable_sequence_number,
                                           validate="key",
                                           validatecommand=self.input_rules.validate_address_sequence)

        self.entry_type_code = Entry(self.container_widget,
                                     textvariable=self.variable_type_code,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_address_type_code)

        self.entry_type_description = Entry(self.container_widget,
                                            textvariable=self.variable_type_description,
                                            validate="key",
                                            validatecommand=self.input_rules.validate_address_type_description)


class PersonLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_first_name = Label(self.container_widget, padding=2, text="First Name")
        self.label_last_name = Label(self.container_widget, padding=2, text="Last Name")
        self.label_middle_initial = Label(self.container_widget, padding=2, text="Middle Initial")
        self.label_nick_name = Label(self.container_widget, padding=2, text="Nick Name")
        self.label_date_of_birth = Label(self.container_widget, padding=2, text="Birth Date")
        self.label_date_of_death = Label(self.container_widget, padding=2, text="Death Date")


class PersonInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)

        self.variable_last_name = StringVar()
        self.variable_first_name = StringVar()
        self.variable_middle_initial = StringVar()
        self.variable_nick_name = StringVar()
        self.variable_date_of_birth = StringVar()
        self.variable_date_of_death = StringVar()

        # set rules before using them
        self.input_rules.set_person_validate_commands()
        self.input_rules.set_general_validation_commands()

        self.entry_first_name = Entry(self.container_widget, textvariable=self.variable_first_name,
                                      validate="key",
                                      validatecommand=self.input_rules.validate_person_first_name)

        self.entry_last_name = Entry(self.container_widget,
                                     textvariable=self.variable_last_name,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_person_last_name)

        self.entry_middle_initial = Entry(self.container_widget,
                                          textvariable=self.variable_middle_initial,
                                          validate="key",
                                          validatecommand=self.input_rules.validate_person_middle_ini)

        self.entry_nick_name = Entry(self.container_widget,
                                     textvariable=self.variable_nick_name,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_person_nickname)

        self.entry_date_of_birth = Entry(self.container_widget,
                                         textvariable=self.variable_date_of_birth,
                                         validate="key",
                                         validatecommand=self.input_rules.validate_date)

        self.entry_date_of_death = Entry(self.container_widget,
                                         textvariable=self.variable_date_of_death,
                                         validate="key",
                                         validatecommand=self.input_rules.validate_date)


class PhoneLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.phone_container = Frame(self.container_widget)
        self.label_area_code = Label(self.phone_container, text="Area Code")
        self.label_exchange = Label(self.phone_container, text="Exchange")
        self.label_trunk = Label(self.phone_container, text="Trunk")
        self.label_phone = Label(self.container_widget, text="Phone Number")
        self.label_sequence_number = Label(self.container_widget, text="Sequence No.")
        self.label_phone_type = Label(self.container_widget, text="Type")
        self.label_person_id = Label(self.container_widget, text="Person Id")
        self.label_contact_id = Label(self.container_widget, text="Contact Id")


class PhoneInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.phone_container = Frame(self.container_widget)
        self.input_rules = InputValidation(container_widget)

        self.variable_person_id = StringVar()
        self.variable_contact_id = StringVar()
        self.variable_phone_type = IntVar()
        self.variable_sequence_number = IntVar()
        self.variable_area_code = StringVar()
        self.variable_exchange = StringVar()
        self.variable_trunk = StringVar()

        self.input_rules.set_phone_validation_commands()
        self.input_rules.set_general_validation_commands()

        self.entry_area_code = Entry(self.phone_container, textvariable=self.variable_area_code,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_phone_area)

        self.entry_exchange = Entry(self.phone_container,
                                    textvariable=self.variable_exchange,
                                    validate="key",
                                    validatecommand=self.input_rules.validate_phone_exchange)

        self.entry_trunk = Entry(self.phone_container,
                                 textvariable=self.variable_trunk,
                                 validate="key",
                                 validatecommand=self.input_rules.validate_phone_trunk)

        self.entry_sequence_number = Entry(self.container_widget,
                                           textvariable=self.variable_sequence_number,
                                           validate="key",
                                           validatecommand=self.input_rules.validate_phone_sequence)

        self.entry_phone_type = Entry(self.container_widget,
                                      textvariable=self.variable_phone_type)

        self.entry_person_id = Entry(self.container_widget,
                                     textvariable=self.variable_person_id,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_integer)

        self.entry_contact_id = Entry(self.container_widget, textvariable=self.variable_contact_id,
                                      validate="key",
                                      validatecommand=self.input_rules.validate_integer)


class EmailLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_email_address = Label(self.container_widget, text="Email Address")
        self.label_sequence_number = Label(self.container_widget, text="Sequence No.")
        self.label_email_type = Label(self.container_widget, text="Type")
        self.label_person_id = Label(self.container_widget, text="Person Id")
        self.label_contact_id = Label(self.container_widget, text="Contact Id")


class EmailInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)

        self.variable_person_id = StringVar()
        self.variable_contact_id = StringVar()
        self.variable_email_address = StringVar()
        self.variable_sequence_number = IntVar()
        self.variable_email_type = IntVar()

        self.input_rules.set_email_validation_commands()
        self.input_rules.set_general_validation_commands()

        self.entry_email_address = Entry(self.container_widget,
                                         textvariable=self.variable_email_address,
                                         validate="key",
                                         validatecommand=self.input_rules.validate_email_address)

        self.entry_sequence_number = Entry(self.container_widget,
                                           textvariable=self.variable_sequence_number,
                                           validate="key",
                                           validatecommand=self.input_rules.validate_email_sequence)

        self.entry_email_type = Entry(self.container_widget,
                                      textvariable=self.variable_email_type)

        self.entry_person_id = Entry(self.container_widget,
                                     textvariable=self.variable_person_id,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_integer)

        self.entry_contact_id = Entry(self.container_widget, textvariable=self.variable_contact_id,
                                      validate="key",
                                      validatecommand=self.input_rules.validate_integer)


class IdentityLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_person_id = Label(self.container_widget, padding=2, text="Person Id")
        self.label_identification_number = Label(self.container_widget, padding=2, text="ID No.")
        self.label_identification_type_id = Label(self.container_widget, padding=2, text="ID Type")
        self.label_issuing_authority = Label(self.container_widget, padding=2, text="Issuing Authority")
        self.label_issuing_entity = Label(self.container_widget, padding=2, text="Issuing Entity")
        self.label_record_location = Label(self.container_widget, padding=2, text="Record Location")
        self.label_identification_id = Label(self.container_widget, padding=2, text="Identifier")
        self.label_type_code = Label(self.container_widget, padding=2, text="Type")
        self.label_type_description = Label(self.container_widget, padding=2, text="Description")


class IdentityInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)

        self.variable_person_id = StringVar()
        self.variable_identification_number = StringVar()
        self.variable_issuing_authority = StringVar()
        self.variable_issuing_entity = StringVar()
        self.variable_record_location = StringVar()
        self.variable_identification_id = IntVar()
        self.variable_type_code = IntVar()
        self.variable_type_description = StringVar()

        self.input_rules.set_identification_validation_commands()
        self.input_rules.set_general_validation_commands()

        self.entry_person_id = Entry(self.container_widget,
                                     textvariable=self.variable_person_id,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_integer)

        self.entry_identification_number = Entry(self.container_widget,
                                                 textvariable=self.variable_identification_number,
                                                 validate="key",
                                                 validatecommand=self.input_rules.validate_id_number)

        self.entry_issuing_authority = Entry(self.container_widget,
                                             textvariable=self.variable_issuing_authority,
                                             validate="key",
                                             validatecommand=self.input_rules.validate_id_authority)

        self.entry_issuing_entity = Entry(self.container_widget,
                                          textvariable=self.variable_issuing_entity,
                                          validate="key",
                                          validatecommand=self.input_rules.validate_id_entity)

        self.entry_record_location = Entry(self.container_widget,
                                           textvariable=self.variable_record_location,
                                           validate="key",
                                           validatecommand=self.input_rules.validate_id_record)

        self.entry_identification_id = Entry(self.container_widget,
                                             textvariable=self.variable_identification_id,
                                             validate="key",
                                             validatecommand=self.input_rules.validate_integer)

        self.entry_type_code = Entry(self.container_widget,
                                     textvariable=self.variable_type_code,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_integer)

        self.entry_type_description = Entry(self.container_widget,
                                            textvariable=self.variable_type_description,
                                            validate="key",
                                            validatecommand=self.input_rules.validate_address_type_description)


class CommentLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_comment = Label(self.container_widget, text="Comment")
        self.label_person_id = Label(self.container_widget, text="Person Id")
        self.label_comment_id = Label(self.container_widget, text="Comment Id")


class CommentsInputs:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)

        self.variable_comment = StringVar()
        self.variable_person_id = StringVar()
        self.variable_comment_id = IntVar()

        self.text_comment = Text(self.container_widget)

        self.entry_person_id = Entry(self.container_widget,
                                     textvariable=self.variable_person_id,
                                     validate="key",
                                     validatecommand=self.input_rules.validate_integer)

        self.entry_comment_id = Entry(self.container_widget,
                                      textvariable=self.variable_comment_id,
                                      validate="key",
                                      validatecommand=self.input_rules.validate_integer)


class SearchLabels:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.label_search_name = Label(self.container_widget, text="Name")
        self.label_search_address = Label(self.container_widget, text="Address")
        self.label_search_birth_date = Label(self.container_widget, text="Birthday")
        self.label_search_comment = Label(self.container_widget, text="Comments")
        self.label_search_box = Label(self.container_widget, text="Comments")


class SearchInputs:
    def __init__(self, container_widget):

        self.filter_choices = ["Select Filter", "First Name", "Last Name", "Address 1", "Address 2",
                               "City", "State", "Zip Code", "Phone", "Email", "Identification", "All"]
        self.container_widget = container_widget
        self.input_rules = InputValidation(container_widget)

        self.variable_search_name = StringVar()
        self.variable_search_address = StringVar()
        self.variable_search_birth_date = StringVar()
        self.variable_search_comment = StringVar()
        self.variable_search_box = StringVar()
        self.variable_radio_option = IntVar()
        self.variable_search_option = StringVar()

        self.input_rules.set_search_input_validation_commands()
        self.entry_search_box = Entry(self.container_widget,
                                      textvariable=self.variable_search_box,
                                      validate="key",
                                      validatecommand=self.input_rules.validate_search_box)
        self.radio_contains = Radiobutton(self.container_widget, text="Contains",
                                          variable=self.variable_radio_option, value=2)
        self.radio_equals = Radiobutton(self.container_widget, text="Equals ", value=1,
                                        variable=self.variable_radio_option)

        self.search_option_menu = OptionMenu(self.container_widget, self.variable_search_option,
                                             self.filter_choices[0],
                                             *self.filter_choices,
                                             command=self.clear_search_box)
        self.search_option_menu.config(width=10)

        self.search_button = Button(self.container_widget, text="Search")

    def clear_search_box(self, selected_value):
        if selected_value == "Select Filter":
            self.variable_search_box.set("")


class RecordButtons:
    def __init__(self, container_widget):
        self.container_widget = container_widget
        self.save = Button(self.container_widget, text="Save")
        self.delete = Button(self.container_widget, text="Delete")
        self.cancel = Button(self.container_widget, text="Cancel")
        self.confirm = Button(self.container_widget, text="Confirm")


#  CONTROL GLOBAL FUNCTIONS
def sort_by_column(tree, col, descending):
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # reorder data
    data.sort(reverse=descending)
    for item_index, item in enumerate(data):
        tree.move(item[1], '', item_index)

    # switch the heading so that it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sort_by_column(tree, col, int(not descending)))
