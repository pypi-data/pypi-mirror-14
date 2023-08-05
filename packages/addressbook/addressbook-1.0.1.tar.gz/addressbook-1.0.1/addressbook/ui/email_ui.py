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

from addressbook.data.create import create_email_contact
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.data.update import update_email_contact
from addressbook.models.contacts import Email
from addressbook.ui.controls import EmailInputs
from addressbook.ui.controls import EmailLabels
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_email_ui


class EmailUi:
    """ Email Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.top_level.wm_title("Email Entry")
        self.mode = mode
        self.person_id = None
        self.labels = EmailLabels(self.top_level)
        self.inputs = EmailInputs(self.top_level)
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)
        self.email_codes = []

        # BUTTONS
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.config(command=self.save_email)
        self.buttons.cancel.config(command=self.quit)

        self.email_codes = []
        self.email_type_list = self.get_email_codes()
        self.email_type_option_variable = StringVar(top_level)

        self.email_type_options = OptionMenu(self.top_level, self.email_type_option_variable,
                                             self.email_type_list[0],
                                             *self.email_type_list, command=self.set_type_id)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_email_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Labels
        self.label_action_status.grid(row=0, column=0, columnspan=2, sticky=EW)
        self.labels.label_email_address.grid(row=1, column=0, sticky=W)
        self.labels.label_sequence_number.grid(row=2, column=0, sticky=W)
        self.labels.label_email_type.grid(row=3, column=0, sticky=W)

        # Entry Inputs
        self.inputs.entry_email_address.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_sequence_number.grid(row=2, column=1, sticky=EW)
        self.inputs.entry_email_type.grid(row=3, column=1, sticky=EW)

        self.email_type_options.grid(row=3, column=1, sticky=EW)

        # Buttons: Insert & Save
        if self.mode == "insert" or self.mode == "update":
            fn = self.parent_top_level.person_inputs.variable_first_name.get()
            ln = self.parent_top_level.person_inputs.variable_last_name.get()
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

    def save_email(self):
        e = Email()
        if self.validate_email():
            e.sequence_number = self.inputs.variable_sequence_number.get()
            e.contact_id = self.inputs.variable_contact_id.get()
            e.email_address = self.inputs.variable_email_address.get()
            e.type_code = self.inputs.variable_email_type.get()
            e.person_id = self.person_id
            if self.mode == "insert":
                if create_email_contact(e):
                    self.label_action_status.config(background="green", foreground="white",
                                                    text="Success! Email saved.")
                    self.buttons.cancel.config(text="Close")
                    self.parent_top_level.fill_tree_email(self.parent_top_level.tree_person_row_iid)
                else:
                    self.label_action_status.config(background="red", foreground="white",
                                                    text="Error: Email not saved.")
            elif self.mode == "update":
                if update_email_contact(e):
                    self.label_action_status.config(background="green", foreground="white",
                                                    text="Success! Email updated.")
                    self.buttons.cancel.config(text="Close")
                    self.parent_top_level.fill_tree_email(self.parent_top_level.tree_person_row_iid)
                else:
                    self.label_action_status.config(background="red", foreground="white",
                                                    text="Error - Email not updated.")

    def quit(self):
        self.top_level.destroy()

    def validate_email(self):
        validation_result = False
        email_is_valid = False
        sequence_is_valid = False
        email_type_is_valid = False
        try:
            if self.person_id is not None:
                if len(self.inputs.variable_email_address.get()) > 0:
                    email_is_valid = True
                if self.inputs.variable_sequence_number.get() > 0:
                    sequence_is_valid = True
                if self.inputs.variable_email_type.get() > 0 \
                        and self.email_type_option_variable.get() != "PLEASE-SELECT":
                    email_type_is_valid = True

            if email_is_valid and sequence_is_valid and email_type_is_valid:
                validation_result = True

            if not sequence_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Sequence must be a number greater than zero")
            if not email_type_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Email type is not valid.")
            if not email_is_valid:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Email is not valid.")
            return validation_result
        except ValueError:
            validation_result = False
            self.label_action_status.config(background="red", foreground="white",
                                            text="Error! Value not valid for input")
            return validation_result

    def get_email_codes(self):
        self.email_codes = read_lookup_code_by_reference("email")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in self.email_codes:
            choices.append(code.type_description)
        return choices

    def set_type_id(self, event):
        for c in self.email_codes:
            if c.type_description == self.email_type_option_variable.get():
                self.inputs.variable_email_type.set(c.type_id)

    def set_selected_choice(self):
        for c in self.email_codes:
            if c.type_id == self.inputs.variable_email_type.get():
                self.email_type_option_variable.set(c.type_description)
