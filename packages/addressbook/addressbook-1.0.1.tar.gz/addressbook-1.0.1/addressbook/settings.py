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


# NOTE: DEPLOYMENT TOP PYPI REQUIRES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  database_name = "pim.db"

# Database Name
database_name = "pim.db"

# Database path
# database_path = "some path"

# Search result row limit:
# This setting prevents the entire database from being returned
# to the user interface when clicking the search button(s).
# Note: Adjusting the size to a very large number may cause performance
#       issues depending on your hardware, memory, and available CPU speed.
#       The number should never need to be too large anyway, given,
#       filtering can be used to get a good set of records returned.

search_result_row_limit = 1000

# Adjust the size of windows to meet your system requirements here.
# Size units are TKINTER (ttk) sizes and vary depending on operating system

# NNN x NNN = Width x Height  as (WxH)
size_about_ui = "500x400"
size_address_ui = "265x275"
size_comment_ui = "400x230"
size_dashboard_ui = "727x545"
size_email_ui = "275x120"
size_help_ui = "800x400"
size_identity_ui = "325x160"
size_person_ui = "245x185"
size_phone_ui = "250x120"
size_relation_ui = "727x250"



