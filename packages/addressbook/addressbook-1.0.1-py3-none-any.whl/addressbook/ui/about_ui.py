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
from addressbook.about import about_software
from addressbook.settings import size_about_ui


class AboutUi:
    """ About UI"""
    def __init__(self, top_level, parent_top_level):
        self.top_level = top_level
        self.parent_top_level = parent_top_level
        self.top_level.wm_title("About Address Book")
        self.about_text = Text(self.top_level)
        self.scroll_bar = Scrollbar(self.top_level)

    def apply_layout(self):

        # Set window size
        self.top_level.geometry(size_about_ui)  # (WxH)
        self.about_text.grid(row=0, column=0, sticky=NSEW)
        # Set weight to make entry widgets stretch to fill column
        Grid.columnconfigure(self.top_level, 0, weight=1)
        Grid.rowconfigure(self.top_level, 0, weight=1)
        self.about_text.insert('1.0', about_software)
        self.scroll_bar.config(command=self.about_text.yview)
        self.about_text.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.grid(row=0, column=2, sticky=NSEW)

    def quit(self):
        self.top_level.destroy()
