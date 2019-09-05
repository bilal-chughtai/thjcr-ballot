#TODO: make this not a copy pasted roomdataparser
class UserDataParser:
    """ Reads a Google Sheet containing users and returns a dictionary of form crsid: dict of attributes """

    def __init__(self, gspread_sheet, sheet_columns_mapping, logger):
        self._logger = logger
        self._parsed_users = {}
        CRSid_column = sheet_columns_mapping['CRSid']
        self._parse_sheet(gspread_sheet, CRSid_column, sheet_columns_mapping)

    def get_users(self):
        return self.users

    def add_attribute(self, CRSid, attribute, attribute_value):
        self._parsed_users[CRSid][attribute] = attribute_value

    def __ne__(self, other_parsed_sheet):
        """ For python2 compatibility """
        return not self.__eq__(other_parsed_sheet)

    def _parse_sheet(self, gspread_sheet, CRSid_column, columns_mapping):

        for row in gspread_sheet.get_all_values()[1:]: #omit the header row
            CRSid = row[CRSid_column]
            user_attributes = self._parse_sheet_row_to_user_attributes(row, columns_mapping)
            self._parsed_users[CRSid] = user_attributes  # includes room name in here

    def _parse_sheet_row_to_user_attributes(self, row, columns_mapping):
        user_attributes = {}
        for attribute in columns_mapping:
            if attribute != "CRSid":
                attribute_index = columns_mapping[attribute]

                # ignore attributes that have been given a -1 index, ie. ignore this attribute
                if attribute_index == -1:  # signal values to ignore
                    # TODO remove this hardcoded attribute if allowed by the frontend requirements
                    user_attributes[attribute] = ''  # but this attr may be hard coded in somewhere...
                else:
                    user_attributes[attribute] = row[attribute_index]
        return user_attributes