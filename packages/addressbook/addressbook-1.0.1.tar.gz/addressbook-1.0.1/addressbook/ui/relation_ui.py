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
from tkinter import messagebox
from tkinter.ttk import *

from addressbook.data.create import create_relation
from addressbook.data.read import read_lookup_code_by_reference
from addressbook.data.read import read_people
from addressbook.data.read import read_relationship_map
from addressbook.data.read import search_people_1
from addressbook.data.read import search_people_2
from addressbook.models.people import Relationship
from addressbook.ui.controls import RecordButtons
from addressbook.ui.controls import SearchInputs
from addressbook.ui.controls import SearchLabels
from addressbook.ui.controls import sort_by_column
from addressbook.settings import size_relation_ui

class RelationUi:
    """Relationship Entry UI"""
    def __init__(self, top_level, mode, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.mode = mode
        self.person_id = None  # Person ID from the main person window
        self.tree_person_row_iid = None  # The person id of the relative that was selected
        self.default_background_color = self.top_level.cget("bg")

        self.search_bar_frame = Frame(self.top_level)

        # Controls
        self.labels = SearchLabels(self.search_bar_frame)
        self.inputs = SearchInputs(self.search_bar_frame)
        # Frames
        self.search_bar_frame.columnconfigure(0, weight=0)
        self.search_bar_frame.columnconfigure(1, weight=0)
        self.search_bar_frame.columnconfigure(2, weight=0)
        self.search_bar_frame.columnconfigure(3, weight=5)
        self.search_bar_frame.columnconfigure(4, weight=0)

        # Search Bar
        self.inputs.search_button.configure(command=self.get_search_results)

        # Relationships
        self.relation_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.relation_container)

        self.relation_choices = self.get_relation_codes()
        self.relation_options_variable = StringVar()
        self.relation_options = OptionMenu(self.relation_container,
                                           self.relation_options_variable,
                                           self.relation_choices[0],
                                           *self.relation_choices)
        self.buttons.save.configure(command=self.save_relationship)

        # Tree View
        self.tree_person = Treeview(self.top_level,  columns=("firstname", "lastname", "middleinitial",
                                                              "nickname", "dateofbirth", "dateofdeath"))
        self.label_action_status = Label(self.top_level, text="", relief=RIDGE)
        self.person_scroll_bar = Scrollbar(self.top_level)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_relation_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)
        Grid.rowconfigure(self.top_level, 2, weight=1)

        # Labels
        self.label_action_status.grid(row=0, column=0, sticky=NSEW, columnspan=4)
        self.inputs.search_option_menu.grid(row=1, column=0)
        self.inputs.radio_contains.grid(row=1, column=1)
        self.inputs.radio_equals.grid(row=1, column=2)
        self.inputs.entry_search_box.grid(row=1, column=3, sticky=EW)
        self.inputs.search_button.grid(row=1, column=4, sticky=EW)
        self.search_bar_frame.grid(row=1, column=1, sticky=EW, columnspan=3)

        # Inputs
        self.tree_person.grid(row=2, column=0, columnspan=3,  sticky=NSEW)
        self.relation_container.grid(row=3, column=0, columnspan=2, sticky=W)
        self.buttons.save.grid(row=1, column=0, sticky=EW)
        self.relation_options.grid(row=1, column=1, sticky=EW)
        self.relation_options.config(width=20)
        self.build_person_tree()

        # People scroll bar
        self.person_scroll_bar.config(command=self.tree_person.yview)
        self.person_scroll_bar.grid(row=2, column=3, sticky=NSEW)
        self.tree_person.config(yscrollcommand=self.person_scroll_bar.set)

    def get_search_results(self):
        # get search results
        search_option = self.inputs.variable_search_option.get()
        search_value = self.inputs.variable_search_box.get()
        radio_value = self.inputs.variable_radio_option.get()

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
            self.inputs.variable_radio_option.set(2)
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

    def get_relation_codes(self):
        relation_codes = read_lookup_code_by_reference("relation")
        choices = []
        choices.append("PLEASE-SELECT")
        for code in relation_codes:
            choices.append(code.type_description)
        return choices

    def save_relationship(self):
        # Mapped relationships are straight forward. For example:
        # 1. Person to assign a relation is picked from the main form.
        # 2. On the relationship form a person to relate is selected
        # 3. If the relationship selected is a child THEN
        # 4. The person to assign is automatically a parent THEREFORE
        # 5. Lookup the integer value for PARENT from the relationship map.
        # This means the relationship to the target of the relation assignment is child
        # AND the target is parent.
        # Or more simply put, if the picked person is marked as a child then
        # the person for whom we are assigning a relation is automatically parent.
        # To keep it straight we simply use a relation ship map to look for the value
        # of parent when child is selected as the relationship to add.

        # Before we do any work stop if a relationship choice was not made.
        if self.relation_options_variable.get() == "PLEASE-SELECT":
            self.label_action_status.config(background="yellow", foreground="black",
                                            text="Please choose a relationship type.")
            return

        relationship_map = read_relationship_map()
        relationship = Relationship()

        # selected_relationship_type = 0  # The integer value of the choice.
        selected_relationship_type_value = ""  # The string value of the choice.
        mapped_relationship_value = ""

        for key in relationship_map:
            if key == self.relation_options_variable.get():
                selected_relationship_type = relationship_map[key]
                selected_relationship_type_value = selected_relationship_type[2]
                mapped_relationship_value = relationship_map[selected_relationship_type[1]][2]

        relationship.person_id = self.person_id
        relationship.related_person_id = self.tree_person_row_iid
        relationship.relationship_type = mapped_relationship_value
        relationship.relationship_type_description = self.relation_options_variable.get()
        relationship.related_person_relationship_type = selected_relationship_type_value

        if relationship.person_id == relationship.related_person_id:
            self.label_action_status.config(background="yellow", foreground="black",
                                            text="The person and related person cannot be the same.")
        else:
            if self.tree_person_row_iid is None:
                self.label_action_status.config(background="yellow", foreground="black",
                                                text="Nothing Selected! Please select a person.")
            else:
                if create_relation(relationship):
                    self.label_action_status.config(background="green", foreground="white",
                                                    text="Success - Relationship Saved!")

                    self.parent_top_level.fill_tree_relationships(self.person_id)
                else:
                    self.label_action_status.config(background="yellow", foreground="black",
                                                    text="Oops... Relationship was not saved.")

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

        # Event Bindings
        self.tree_person.bind('<<TreeviewSelect>>', self.person_row_selected)
        peo = read_people()
        for person in peo:
            self.tree_person.insert("", "end", iid=person.person_id,
                                    values=[person.first_name, person.last_name, person.middle_initial,
                                            person.nick_name, person.date_of_birth,
                                            person.date_of_death])
            self.tree_person.column("firstname", width=75, anchor=W)
            self.tree_person.column("lastname", width=75, anchor=W)
            self.tree_person.column("middleinitial", width=75, anchor=W)
            self.tree_person.column("nickname", width=75, anchor=W)
            self.tree_person.column("dateofbirth", width=75, anchor=W)
            self.tree_person.column("dateofdeath", width=75, anchor=W)
            self.tree_person["show"] = "headings"
            # self.tree_person["displaycolumns"] = [4, 8, 9, 18]

    def person_row_selected(self, event):
        self.tree_person_row_iid = self.tree_person.focus()
        if self.tree_person_row_iid == self.person_id:
            self.label_action_status.config(background="yellow", foreground="black",
                                            text="The person and related person cannot be the same.")
        else:
            self.label_action_status.config(background=self.default_background_color, text="")

    def quit(self):
        self.top_level.destroy()
