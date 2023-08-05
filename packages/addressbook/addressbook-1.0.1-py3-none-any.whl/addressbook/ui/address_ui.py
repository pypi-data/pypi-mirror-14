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


"""
Address User Interfaces.

"""

from tkinter import *
from tkinter.ttk import *

from addressbook.data.create import create_address
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.models.addresses import Address
from addressbook.ui.controls import AddressInputs
from addressbook.ui.controls import AddressLabels
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_address_ui


class AddressUi:
    """Address Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.top_level.wm_title("Address Entry")
        self.person_id = None
        self.mode = mode
        self.inputs = AddressInputs(self.top_level)
        self.labels = AddressLabels(self.top_level)

        # BUTTONS
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.config(command=self.save_address)
        self.buttons.cancel.config(command=self.quit)
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)
        self.default_background_color = self.top_level.cget("bg")
        self.address_codes = []
        self.address_type_list = self.get_address_codes()
        self.address_type_list.insert(0, 'PLEASE-SELECT')
        self.address_type_option_variable = StringVar(top_level)
        self.address_type_options = OptionMenu(self.top_level, self.address_type_option_variable,
                                               self.address_type_list[0],
                                               *self.address_type_list)

    def apply_layout(self):
        """
        Applies the UI layout.
        """
        # Set window size
        self.top_level.geometry(size_address_ui)  # (W x H)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Labels
        self.label_action_status.grid(row=0, column=0, columnspan=2, sticky=EW)
        self.labels.label_address_line_1.grid(row=1, column=0, sticky=W)
        self.labels.label_address_line_2.grid(row=2, column=0, sticky=W)
        self.labels.label_po_box.grid(row=3, column=0, sticky=W)
        self.labels.label_city.grid(row=4, column=0, sticky=W)
        self.labels.label_state.grid(row=5, column=0, sticky=W)
        self.labels.label_zip_code.grid(row=6, column=0, sticky=W)
        self.labels.label_zip_4.grid(row=7, column=0, sticky=W)
        self.labels.label_postal_code.grid(row=8, column=0, sticky=W)
        self.labels.label_status.grid(row=9, column=0, sticky=W)
        self.labels.label_address_type_id.grid(row=10, column=0, sticky=W)
        self.labels.label_sequence_number.grid(row=11, column=0, sticky=W)

        # Entry Inputs
        self.inputs.entry_address_line_1.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_address_line_2.grid(row=2, column=1, sticky=EW)
        self.inputs.entry_po_box.grid(row=3, column=1, sticky=EW)
        self.inputs.entry_city.grid(row=4, column=1, sticky=EW)
        self.inputs.entry_state.grid(row=5, column=1, sticky=EW)
        self.inputs.entry_zip_code.grid(row=6, column=1, sticky=EW)
        self.inputs.entry_zip_4.grid(row=7, column=1, sticky=EW)
        self.inputs.entry_postal_code.grid(row=8, column=1, sticky=EW)
        self.inputs.entry_status.grid(row=9, column=1, sticky=EW)
        self.address_type_options.grid(row=10, column=1, sticky=EW)
        self.inputs.entry_sequence_number.grid(row=11, column=1, sticky=EW)

        # Buttons: Insert & Save
        if self.mode == "insert" or self.mode == "update":

            # Set title of window to reflect action
            if self.mode == "insert":
                fn = self.parent_top_level.person_inputs.variable_first_name.get()
                ln = self.parent_top_level.person_inputs.variable_last_name.get()
                title = ("Add: ", fn, " ", ln)
                self.top_level.wm_title("".join(title))
            if self.mode == "update":
                self.top_level.wm_title("Update Address")
            # Set the buttons
            self.button_container.grid(row=12, column=1, pady=(10, 0), sticky=EW)
            self.buttons.save.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)

    def save_address(self):
        self.label_action_status.config(text="", background=self.default_background_color)
        for c in self.address_codes:
            if c.type_description == self.address_type_option_variable.get():
                self.inputs.variable_address_type_id.set(c.type_id)

        if self.validate_address():
            new_address = Address()
            new_address.address_id = None
            new_address.person_id = self.person_id
            new_address.address_line_1 = self.inputs.variable_address_line_1.get()
            new_address.address_line_2 = self.inputs.variable_address_line_2.get()
            new_address.po_box = self.inputs.variable_po_box.get()
            new_address.city = self.inputs.variable_city.get()
            new_address.state = self.inputs.variable_state.get()
            new_address.zip_code = self.inputs.variable_zip_code.get()
            new_address.postal_code = self.inputs.variable_postal_code.get()
            new_address.zip4 = self.inputs.variable_zip_4.get()
            new_address.sequence_number = self.inputs.variable_sequence_number.get()
            new_address.status = self.inputs.variable_status.get()
            new_address.type_code = self.inputs.variable_type_code.get()
            new_address.type_description = self.inputs.variable_type_description.get()
            new_address.type_id = self.inputs.variable_address_type_id.get()
            if create_address(new_address):
                self.parent_top_level.fill_tree_addresses(self.person_id)
                self.label_action_status.config(background="green", foreground="white",
                                                text="Success! Address saved.")
                self.buttons.cancel.config(text="Close")
            else:
                self.label_action_status.config(background="red", foreground="white",
                                                text="Error! Address Not Saved.")

    def quit(self):
        """
        Closes the window.
        """
        self.top_level.destroy()

    def validate_address(self):
        """Address validation rules.
        :return: Boolean indicating if the address is valid.
        """
        validation_result = False
        line1_is_valid = False
        city_is_valid = False
        state_is_valid = False
        zip_is_valid = False
        sequence_is_valid = False
        address_type_is_valid = False

        zip_code = 0
        zip4 = 0
        sequence = 0

        try:
            zip4 = self.inputs.variable_zip_4.get()
        except ValueError:
            self.inputs.variable_zip_4.set(zip4)
        try:
            zip_code = self.inputs.variable_zip_code.get()
        except ValueError:
            self.inputs.variable_zip_code.set(zip_code)
        try:
            sequence = self.inputs.variable_sequence_number.get()
        except ValueError:
            self.inputs.variable_sequence_number.set(sequence)
        try:
            if self.person_id is not None:
                if len(self.inputs.variable_address_line_1.get()) > 0:
                    line1_is_valid = True
                if len(self.inputs.variable_city.get()) > 0:
                    city_is_valid = True
                if len(self.inputs.variable_state.get()) > 0:
                    state_is_valid = True
                if zip_code > 0:
                    zip_is_valid = True
                if sequence > 0:
                    sequence_is_valid = True
                if self.inputs.variable_address_type_id.get() > 0:
                    address_type_is_valid = True
                if line1_is_valid and \
                        city_is_valid and \
                        state_is_valid and \
                        zip_is_valid and \
                        address_type_is_valid and \
                        sequence_is_valid:
                    validation_result = True

            if not sequence_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Sequence must be a number greater than zero")
            if not address_type_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Address type is invalid.")
            if not zip_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Zip code is not valid.")
            if not state_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="State is required.")
            if not city_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="City is required.")
            if not line1_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Address line 1 is required.")
        except ValueError:
            validation_result = False
            self.label_action_status.config(background="red", foreground="white",
                                            text="Error! Value not valid for input")
        return validation_result

    def get_address_codes(self):
        """
        :return: List of Codes() for address type options.
        """
        self.address_codes = read_lookup_code_by_reference("address")
        choices = []
        for code in self.address_codes:
            choices.append(code.type_description)
        return choices
