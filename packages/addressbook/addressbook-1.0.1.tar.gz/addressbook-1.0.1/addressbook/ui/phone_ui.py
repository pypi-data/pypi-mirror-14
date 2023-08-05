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

from addressbook.data.create import create_phone_contact
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.data.update import update_phone_contact
from addressbook.models.contacts import Phone
from addressbook.ui.controls import PhoneInputs
from addressbook.ui.controls import PhoneLabels
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_phone_ui


class PhoneUi:
    """ Phone Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.top_level.wm_title("Phone Entry")
        self.mode = mode
        self.person_id = None
        self.labels = PhoneLabels(self.top_level)
        self.inputs = PhoneInputs(self.top_level)
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)

        # Buttons
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.config(command=self.save_phone)
        self.buttons.cancel.config(command=self.quit)

        self.phone_codes = []
        self.phone_type_list = self.get_phone_codes()
        self.phone_type_option_variable = StringVar(top_level)

        self.phone_type_options = OptionMenu(self.top_level, self.phone_type_option_variable,
                                             self.phone_type_list[0],
                                             *self.phone_type_list, command=self.set_type_id)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_phone_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Phone container
        self.label_action_status.grid(row=0, column=0, columnspan=2, sticky=EW)
        self.inputs.phone_container.grid(row=1, column=1, sticky=EW)

        # Labels
        self.labels.label_phone.grid(row=1, column=0)
        self.labels.label_area_code.grid(row=1, column=0, sticky=EW)
        self.labels.label_exchange.grid(row=1, column=1, sticky=EW)
        self.labels.label_trunk.grid(row=1, column=2, sticky=EW)

        self.labels.label_sequence_number.grid(row=2, column=0, sticky=W)
        self.labels.label_phone_type.grid(row=3, column=0, sticky=W)

        # Entry Inputs
        self.inputs.entry_area_code.config(width=6)
        self.inputs.entry_exchange.config(width=6)
        self.inputs.entry_trunk.config(width=7)
        self.inputs.entry_area_code.grid(row=1, column=0, sticky=EW)
        self.inputs.entry_exchange.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_trunk.grid(row=1, column=2, sticky=EW)
        self.inputs.entry_sequence_number.grid(row=2, column=1, sticky=W)
        self.phone_type_options.grid(row=3, column=1, sticky=EW)

        # Buttons: Insert & Save
        if self.mode == "insert" or self.mode == "update":
            fn = self.parent_top_level.person_inputs.variable_first_name.get()
            ln = self.parent_top_level.person_inputs.variable_last_name.get()
            # Set title of window to reflect action
            if self.mode == "insert":
                title = ("Add: ", fn, " ", ln)
                self.top_level.wm_title("".join(title))
            if self.mode == "update":
                title = ("Update: ", fn, " ", ln)
                self.top_level.wm_title("".join(title))
                self.set_selected_choice()

            # Set the buttons
            self.button_container.grid(row=5, column=1, pady=(10, 0), sticky=EW)
            self.buttons.save.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)
            # Configure weights
            self.button_container.columnconfigure(0, weight=1)
            self.button_container.columnconfigure(1, weight=1)

    def save_phone(self):
        ph = Phone()
        if self.validate_phone():
            ph.type_code = self.inputs.variable_phone_type.get()
            ph.person_id = self.person_id
            ph.area_code = self.inputs.variable_area_code.get()
            ph.exchange = self.inputs.variable_exchange.get()
            ph.trunk = self.inputs.variable_trunk.get()
            ph.sequence_number = self.inputs.variable_sequence_number.get()
            ph.contact_id = self.inputs.variable_contact_id.get()
            if self.mode == "insert":
                if create_phone_contact(ph):
                    self.label_action_status.config(background="green", foreground="white",
                                                    text="Success! Phone saved.")
                    self.buttons.cancel.config(text="Close")
                    self.parent_top_level.fill_tree_phone_numbers(self.parent_top_level.tree_person_row_iid)
                else:
                    self.label_action_status.config(background="red", foreground="white",
                                                    text="Error! Phone not saved.")
            elif self.mode == "update":
                if update_phone_contact(ph):
                    self.label_action_status.config(background="green", foreground="white",
                                                    text="Success! Phone updated.")
                    self.parent_top_level.fill_tree_phone_numbers(self.parent_top_level.tree_person_row_iid)
                    self.buttons.cancel.config(text="Close")
                else:
                    self.label_action_status.config(background="red", foreground="white",
                                                    text="Error! Phone not updated.")

    def quit(self):
        self.top_level.destroy()

    def validate_phone(self):
        validation_result = False
        phone_number_is_valid = False
        sequence_is_valid = False
        phone_type_is_valid = False
        try:
            if self.person_id is not None:
                area = self.inputs.variable_area_code.get()
                exchange = self.inputs.variable_exchange.get()
                trunk = self.inputs.variable_trunk.get()

                if area.isdigit() and exchange.isdigit() and trunk.isdigit():
                    if len(area) == 3 and len(exchange) == 3 and len(trunk) == 4:
                        phone_number_is_valid = True
                if self.inputs.variable_sequence_number.get() > 0:
                    sequence_is_valid = True
                if self.inputs.variable_phone_type.get() > 0 \
                        and self.phone_type_option_variable.get() != "PLEASE-SELECT":
                    phone_type_is_valid = True

            if phone_number_is_valid and sequence_is_valid and phone_type_is_valid:
                validation_result = True

            if not phone_type_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Phone type is not valid.")
            if not sequence_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Sequence number is not valid.")
            if not phone_number_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Phone number is not valid.")
            return validation_result
        except ValueError:
            validation_result = False
            self.label_action_status.config(background="red", foreground="white",
                                            text="Error! Value not valid for input")
            return validation_result

    def get_phone_codes(self):
        self.phone_codes = read_lookup_code_by_reference("phone")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in self.phone_codes:
            choices.append(code.type_description)
        return choices

    def set_type_id(self, event):
        for c in self.phone_codes:
            if c.type_description == self.phone_type_option_variable.get():
                self.inputs.variable_phone_type.set(c.type_id)

    def set_selected_choice(self):
        for c in self.phone_codes:
            if c.type_id == self.inputs.variable_phone_type.get():
                self.phone_type_option_variable.set(c.type_description)
