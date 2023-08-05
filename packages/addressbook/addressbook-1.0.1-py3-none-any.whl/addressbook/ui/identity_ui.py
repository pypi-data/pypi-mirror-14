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

from addressbook.data.create import create_identification
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.models.identities import Identity
from addressbook.ui.controls import IdentityInputs
from addressbook.ui.controls import IdentityLabels
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_identity_ui

class IdentityUi:
    """Identity Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.top_level.wm_title("Identity Entry")
        self.mode = mode
        self.person_id = None
        self.labels = IdentityLabels(self.top_level)
        self.inputs = IdentityInputs(self.top_level)
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)

        # Buttons
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.config(command=self.save_identity)
        self.buttons.cancel.config(command=self.quit)

        self.identity_codes = []
        self.identity_type_list = self.get_id_codes()
        self.identity_type_option_variable = StringVar(top_level)

        self.identity_type_options = OptionMenu(self.top_level, self.identity_type_option_variable,
                                                self.identity_type_list[0],
                                                *self.identity_type_list, command=self.set_type_id)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_identity_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Labels
        self.label_action_status.grid(row=0, sticky=EW, columnspan=2)
        self.labels.label_identification_number.grid(row=1, column=0, sticky=W)
        self.labels.label_issuing_authority.grid(row=2, column=0, sticky=W)
        self.labels.label_issuing_entity.grid(row=3, column=0, sticky=W)
        self.labels.label_record_location.grid(row=4, column=0, sticky=W)
        self.labels.label_type_code.grid(row=5, column=0, sticky=W)

        # Entry Inputs
        self.inputs.entry_identification_number.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_issuing_authority.grid(row=2, column=1, sticky=EW)
        self.inputs.entry_issuing_entity.grid(row=3, column=1, sticky=EW)
        self.inputs.entry_record_location.grid(row=4, column=1, sticky=EW)
        self.identity_type_options.grid(row=5, column=1, sticky=EW)

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

            # Set the buttons
            self.button_container.grid(row=7, column=1, pady=(10, 0), sticky=EW)
            self.buttons.save.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)

    def save_identity(self):
        if self.validate_identification():
            identification = Identity()
            identification.person_id = self.person_id
            identification.type_code = self.inputs.variable_type_code.get()
            identification.identification_number = self.inputs.variable_identification_number.get()
            identification.issuing_authority = self.inputs.variable_issuing_authority.get()
            identification.issuing_entity = self.inputs.variable_issuing_entity.get()
            identification.record_location = self.inputs.variable_record_location.get()
            if create_identification(identification):
                self.label_action_status.config(background="green", foreground="white",
                                                text="Success! Identity saved.")
                self.buttons.cancel.config(text="Close")
                self.parent_top_level.fill_tree_identities(self.person_id)
            else:
                self.label_action_status.config(background="red", foreground="white",
                                                text="Error! Identity not saved.")

    def validate_identification(self):
        valid_type_id = False
        valid_id_number = False
        validation_result = False
        try:
            if self.person_id is not None:
                if self.inputs.variable_type_code.get() > 0 \
                        and self.identity_type_option_variable.get() != "PLEASE-SELECT":
                    valid_type_id = True
                if len(self.inputs.variable_identification_number.get()) > 0:
                    valid_id_number = True

                if valid_type_id and valid_id_number:
                    validation_result = True

            if not valid_type_id:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Identification type is not valid.")
            if not valid_id_number:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Identification number is not valid.")
            return validation_result
        except ValueError:
            validation_result = False
            self.label_action_status.config(background="red", foreground="white",
                                            text="Error! Value not valid for input")
            return validation_result

    def quit(self):
        self.top_level.destroy()

    def get_id_codes(self):
        self.identity_codes = read_lookup_code_by_reference("id")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in self.identity_codes:
            choices.append(code.type_description)
        return choices

    def set_type_id(self, event):
        for c in self.identity_codes:
            if c.type_description == self.identity_type_option_variable.get():
                self.inputs.variable_type_code.set(c.type_id)
