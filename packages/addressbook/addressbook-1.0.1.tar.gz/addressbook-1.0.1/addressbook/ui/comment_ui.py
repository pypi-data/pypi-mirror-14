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

from addressbook.ui.controls import CommentLabels
from addressbook.ui.controls import CommentsInputs
from addressbook.ui.controls import RecordButtons
from addressbook.settings import size_comment_ui

class CommentUi:
    """Comment Entry UI"""
    def __init__(self, top_level, parent_person_ui, mode):
        self.top_level = top_level
        self.top_level.wm_title("Comment Entry")
        self.mode = mode
        self.add_comment_to_person(parent_person_ui)
        self.labels = CommentLabels(self.top_level)
        self.inputs = CommentsInputs(self.top_level)

        # Buttons
        self.button_container = Frame(self.top_level)
        self.buttons = RecordButtons(self.button_container)
        self.buttons.save.configure(command=self.add_comment_to_person)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_comment_ui)

        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 1, weight=1)

        # Labels
        self.labels.label_comment.grid(row=0, column=0, sticky=NW)
        self.labels.label_person_id.grid(row=1, column=0, sticky=W)
        self.labels.label_comment_id.grid(row=2, column=0, sticky=W)

        # Entry Inputs
        self.inputs.text_comment.grid(row=0, column=1, sticky=EW)
        self.inputs.entry_person_id.grid(row=1, column=1, sticky=EW)
        self.inputs.entry_comment_id.grid(row=2, column=1, sticky=EW)

        # Buttons:  Insert & Save
        if self.mode == "insert" or self.mode == "update":

            # Set title of window to reflect action
            if self.mode == "insert":
                self.top_level.wm_title("Create Comment")
            if self.mode == "update":
                self.top_level.wm_title("Update Comment")

            # Set the buttons
            self.button_container.grid(row=5, column=1, pady=(10, 0), sticky=EW)
            self.buttons.save.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)

        if self.mode == "delete":
            self.button_container.grid(row=5, column=1, pady=(10, 0), sticky=EW)
            self.buttons.delete.grid(row=0, column=0, sticky=EW)
            self.buttons.cancel.grid(row=0, column=1, sticky=EW)
            self.top_level.wm_title("Delete Comment")

    def add_comment_to_person(self, per_ui):
        """Appends comment to the person UI. (PersonUi)
        :rtype: None
        :param per_ui: Parent UI to append.
        """
        pass
