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
from tkinter import *
from tkinter.ttk import *

from addressbook.data.create import create_person
from addressbook.data.identifiers import random_char
from addressbook.data.read import is_person_identifier_used
from addressbook.models.people import Person
from addressbook.ui.controls import PersonInputs
from addressbook.ui.controls import PersonLabels
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_person_ui


class PersonUi:
    """ Person Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.mode = mode
        self.top_level.wm_title("Person Entry")
        self.person = Person()
        self.labels = PersonLabels(self.top_level)
        self.inputs = PersonInputs(self.top_level)
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.config(command=self.add_person)
        self.buttons.cancel.config(command=self.quit)
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)
        self.default_background_color = self.top_level.cget("bg")

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_person_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Labels
        self.labels.label_first_name.grid(row=1, column=0, sticky=W)
        self.labels.label_last_name.grid(row=2, column=0, sticky=W)
        self.labels.label_middle_initial.grid(row=3, column=0, sticky=W)
        self.labels.label_nick_name.grid(row=4, column=0, sticky=W)
        self.labels.label_date_of_birth.grid(row=5, column=0, sticky=W)
        self.labels.label_date_of_death.grid(row=6, column=0, sticky=W)

        # Entry Inputs
        self.inputs.entry_first_name.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_last_name.grid(row=2, column=1, sticky=EW)
        self.inputs.entry_middle_initial.grid(row=3, column=1, sticky=EW)
        self.inputs.entry_nick_name.grid(row=4, column=1, sticky=EW)
        self.inputs.entry_date_of_birth.grid(row=5, column=1, sticky=EW)
        self.inputs.entry_date_of_death.grid(row=6, column=1, sticky=EW)

        # Buttons: Insert & Save
        if self.mode == "insert" or self.mode == "update":

            # Set title of window to reflect action
            if self.mode == "insert":
                self.top_level.wm_title("Create Person")
            if self.mode == "update":
                self.top_level.wm_title("Update Person")

            # Set the buttons
            self.button_container.grid(row=7, column=1, pady=(10, 0), sticky=EW)
            self.buttons.save.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)
            self.label_action_status.grid(row=0, column=0, sticky=NSEW, columnspan=4)

        # Buttons: Delete & Confirm
        if self.mode == "delete":

            # Set title of window to reflect action
            self.top_level.wm_title("Delete Person")

            # Set the buttons
            self.button_container.grid(row=11, column=1)
            # self.delete_button.grid(row=0, column=0)
            # self.cancel_button.grid(row=0, column=1)

    def add_person(self):
        person = Person()
        person.person_id = random_char(26)
        person.first_name = self.inputs.variable_first_name.get()
        person.last_name = self.inputs.variable_last_name.get()
        person.nick_name = self.inputs.variable_nick_name.get()
        person.middle_initial = self.inputs.variable_middle_initial.get()
        person.date_of_birth = self.inputs.variable_date_of_birth.get()
        person.date_of_death = self.inputs.variable_date_of_death.get()

        # First and last names are required to save. So before save check if provided.
        if len(person.first_name) == 0 or len(person.last_name) == 0:
            self.label_action_status.config(background="yellow", foreground="black", text="First and Last Required")
            return

        # Dates (DOB and DOD) not required but if present must be valid dates.
        # Expected date format is: YYYY-MM-DD
        if len(person.date_of_birth) > 0 or len(person.date_of_death) > 0:
            try:
                date_value = None
                if len(person.date_of_birth) > 0:
                    date_value = person.date_of_birth.split("-")
                if len(person.date_of_death) > 0:
                    date_value = person.date_of_death.split("-")

                datetime.datetime(int(date_value[0]), int(date_value[1]), int(date_value[2]))

            except ValueError:
                self.label_action_status.config(background="red", foreground="white",
                                                text="Date Error: Expected YYYY-MM-DD")
                return
            except IndexError:
                self.label_action_status.config(background="red", foreground="white",
                                                text="Date Error: Expected YYYY-MM-DD")
                return
            except TypeError:
                self.label_action_status.config(background="red", foreground="white",
                                                text="Date Error: Expected YYYY-MM-DD")
                return
        # Before we create a person record we need to make sure that the
        # identifier for the person record has not already been used.
        # If used = yes then get new identifier
        # if used = no then okay to use identifier

        # set an iteration limit here to prevent endless looping as it should be extremely
        # rare, we still want to check if there is a problem if we cannot find an unused
        # random identifier. For example, if we cannot find a random identifier in 5000 tries
        # we need to re-evaluate the use of random for identifiers.
        iteration_limit = 5000
        iterator_value = 0
        while is_person_identifier_used(person.person_id):
            person.person_id = random_char(26)
            iterator_value += 1
            if iterator_value == iteration_limit:
                break
        # if we hit 5000+ then just quit don't try to add a record (UI needs to be notified)
        if iterator_value >= 5000:
            self.label_action_status.config(background="red", foreground="white",
                                            text="Error: Record identifier not found")
            return
        else:
            if create_person(person):
                self.label_action_status.config(background="green", foreground="white", text="Success - Person Saved")
                self.parent_top_level.fill_tree_person()
                self.buttons.cancel.config(text="Close")
            else:
                self.label_action_status.config(background="red", foreground="white", text="Error - Person NOT Saved")

    def quit(self):
        self.top_level.destroy()
