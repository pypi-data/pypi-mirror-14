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
GUI Validation specific to Tkinter Widget Validation
"""


class InputValidation:
    def __init__(self, container_widget):
        """
        Init: Setup
        :param container_widget: Tk as root container
        """
        self.root = container_widget
        # Person Rules
        self.validate_person_first_name = None
        self.validate_person_last_name = None
        self.validate_person_middle_ini = None
        self.validate_person_nickname = None
        self.validate_person_birth = None
        self.validate_person_death = None
        self.validate_person_comment = None
        # Email Rules
        self.validate_email_address = None
        self.validate_email_type = None
        self.validate_email_sequence = None

        # Phone Rules
        self.validate_phone_type = None
        self.validate_phone_area = None
        self.validate_phone_exchange = None
        self.validate_phone_trunk = None
        self.validate_phone_sequence = None

        # Address Rules
        self.validate_address_line_1 = None
        self.validate_address_line_2 = None
        self.validate_address_pobox = None
        self.validate_address_city = None
        self.validate_address_state = None
        self.validate_address_zip = None
        self.validate_address_zip4 = None
        self.validate_address_postal = None
        self.validate_address_sequence = None
        self.validate_address_status = None
        self.validate_address_type_code = None
        self.validate_address_type_description = None
        self.validate_address_type_id = None

        # Identification Rules
        self.validate_id_number = None
        self.validate_id_type_code = None
        self.validate_id_type_description = None
        self.validate_id_authority = None
        self.validate_id_entity = None
        self.validate_id_record = None

        # Search Input Rules
        self.validate_search_box = None

        # General Rules that apply everywhere
        self.validate_date = (self.root.register(self.on_validate_date), '%P', '%S', 10)
        self.validate_integer = (self.root.register(self.on_validate_integer), '%P', '%S', 10)

        # Setup validation commands
        # self.set_validation_commands()

    def on_validate_integer(self, p, s, expected_length):
        """
        On Validate Integer Entry
        :param p: %P = value of the entry if the edit is allowed
        :param s: %S = the text string being inserted or deleted, if any
        :param expected_length: Length of string in widget
        :return: S
        """
        # return_value = None
        if s:
            if len(p) > int(expected_length):
                return_value = None
            else:
                try:
                    int(s)
                    return_value = s
                except ValueError:
                    return_value = None
        else:
            return_value = s  # if not S we are in a state of instantiate and no keys are being pressed.

        return s == return_value

    def on_validate_decimal(self, p, s, expected_length):
        """
        On Validate Decimal Entry
        :param p: %P = value of the entry if the edit is allowed
        :param s: %S = the text string being inserted or deleted, if any
        :param expected_length: Length of string in widget
        :return: S
        """
        # return_value = None
        if s:
            if len(p) > int(expected_length):
                return_value = None
            else:
                try:
                    float(s)
                    return_value = s
                except ValueError:
                    if s in "." and p.count('.') <= 1:
                        return_value = s
                    else:
                        return_value = None
        else:
            return_value = s  # if not S we are in a state of instantiate and no keys are being pressed.

        return s == return_value

    def on_validate_date(self, p, s, expected_length):
        """
        On Validate Date Entry
        :param p: %P = value of the entry if the edit is allowed
        :param s: %S = the text string being inserted or deleted, if any
        :param expected_length: Length of string in widget
        :return: S
        """
        # return_value = None
        if s:
            if len(p) > int(expected_length):
                return_value = None
            else:
                try:
                    float(s)
                    return_value = s
                except ValueError:
                    if s in "-" and p.count('-') <= 2:
                        return_value = s
                    else:
                        return_value = None
        else:
            return_value = s  # if not S we are in a state of instantiate and no keys are being pressed.

        return s == return_value

    def on_validate_length(self, p, s, expected_length):
        """
        On Validate Length of Entry. Pattern match "%'!#$^&*()+={}[]<>;?√"
        :param p: %P = value of the entry if the edit is allowed
        :param s: %S = the text string being inserted or deleted, if any
        :param expected_length: expected_length:
        :return: S
        """
        # return_value = None
        if s:
            if len(p) > int(expected_length):
                return_value = None
            else:
                if s in "%'!#$^&*()+={}[]<>;?√":
                    return_value = None
                else:
                    return_value = s
        else:
            return_value = s  # if not S we are in a state of instantiate and no keys are being pressed.
        return s == return_value

    def set_person_validate_commands(self):
        """
        Private: Sets (creates instances) of command objects for tkinter widget validation.
        """
        # self.command_integer = (self.root.register(self.on_validate_integer), '%P', '%S', 3)

        # Person Rules
        self.validate_person_first_name = (self.root.register(self.on_validate_length), '%P', '%S', 30)
        self.validate_person_last_name = (self.root.register(self.on_validate_length), '%P', '%S', 30)
        self.validate_person_middle_ini = (self.root.register(self.on_validate_length), '%P', '%S', 1)
        self.validate_person_nickname = (self.root.register(self.on_validate_length), '%P', '%S', 20)
        self.validate_person_birth = (self.root.register(self.on_validate_date), '%P', '%S', 10)
        self.validate_person_death = (self.root.register(self.on_validate_date), '%P', '%S', 10)
        # self.command_person_relationship_type = (self.root.register(self.on_validate_length), '%P', '%S', 10)
        self.validate_person_comment = (self.root.register(self.on_validate_length), '%P', '%S', 5)

    def set_email_validation_commands(self):
        # Email Rules
        self.validate_email_address = (self.root.register(self.on_validate_length), '%P', '%S', 100)
        # self.validate_email_type = (self.root.register(self.on_validate_length), '%P', '%S', 2)
        self.validate_email_sequence = (self.root.register(self.on_validate_integer), '%P', '%S', 2)

    def set_phone_validation_commands(self):
        # Phone Rules
        # self.validate_phone_type = (self.root.register(self.on_validate_length), '%P', '%S', 10)
        self.validate_phone_area = (self.root.register(self.on_validate_integer), '%P', '%S', 3)
        self.validate_phone_exchange = (self.root.register(self.on_validate_integer), '%P', '%S', 3)
        self.validate_phone_trunk = (self.root.register(self.on_validate_integer), '%P', '%S', 4)
        self.validate_phone_sequence = (self.root.register(self.on_validate_integer), '%P', '%S', 2)

    def set_address_validation_commands(self):
        # Address Rules
        self.validate_address_line_1 = (self.root.register(self.on_validate_length), '%P', '%S', 64)
        self.validate_address_line_2 = (self.root.register(self.on_validate_length), '%P', '%S', 64)
        self.validate_address_pobox = (self.root.register(self.on_validate_length), '%P', '%S', 30)
        self.validate_address_city = (self.root.register(self.on_validate_length), '%P', '%S', 64)
        self.validate_address_state = (self.root.register(self.on_validate_length), '%P', '%S', 2)
        self.validate_address_zip = (self.root.register(self.on_validate_integer), '%P', '%S', 5)
        self.validate_address_zip4 = (self.root.register(self.on_validate_integer), '%P', '%S', 4)
        self.validate_address_postal = (self.root.register(self.on_validate_length), '%P', '%S', 15)
        self.validate_address_sequence = (self.root.register(self.on_validate_integer), '%P', '%S', 3)
        self.validate_address_status = (self.root.register(self.on_validate_length), '%P', '%S', 5)
        self.validate_address_type_code = (self.root.register(self.on_validate_length), '%P', '%S', 100)
        self.validate_address_type_description = (self.root.register(self.on_validate_length), '%P', '%S', 100)
        self.validate_address_type_id = (self.root.register(self.on_validate_length), '%P', '%S', 100)

    def set_identification_validation_commands(self):
        # Identification Rules
        self.validate_id_number = (self.root.register(self.on_validate_length), '%P', '%S', 20)
        self.validate_id_type_code = (self.root.register(self.on_validate_integer), '%P', '%S', 10)
        self.validate_id_type_description = (self.root.register(self.on_validate_length), '%P', '%S', 20)
        self.validate_id_authority = (self.root.register(self.on_validate_length), '%P', '%S', 30)
        self.validate_id_entity = (self.root.register(self.on_validate_length), '%P', '%S', 30)
        self.validate_id_record = (self.root.register(self.on_validate_length), '%P', '%S', 100)

    def set_general_validation_commands(self):
        # General Rules that apply every where
        self.validate_date = (self.root.register(self.on_validate_date), '%P', '%S', 10)
        self.validate_integer = (self.root.register(self.on_validate_integer), '%P', '%S', 10)

    def set_search_input_validation_commands(self):
        self.validate_search_box = (self.root.register(self.on_validate_length), '%P', '%S', 200)
