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
from addressbook.ui import dashboard_ui
from shutil import copy
import os.path

# If the database already exists DO NOT OVERWRITE
# Otherwise begin with blank database

current_dir = os.getcwd()
blank_db_source = os.path.join(current_dir, "blank.db")
existing_db_source = os.path.join(current_dir, "pim.db")

if not os.path.exists(existing_db_source):
    copy(blank_db_source, existing_db_source)


class Application:
    def __init__(self):
        self.root = Tk()
        self.dashboard = dashboard_ui.DashboardUi(self.root)
        self.dashboard.apply_layout()
        self.root.mainloop()


def main():
    Application()

if __name__ == '__main__':
    main()
