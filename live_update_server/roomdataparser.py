

class RoomDataParser():
    """ Reads a Google Sheet and returns rows parsed into a dictionary form room name : { room attrs } """

    def __init__(self, gspread_sheet, sheet_columns_mapping, room_name_to_svg_id, logger):
        self._logger = logger
        room_name_column = sheet_columns_mapping['roomName']
        self._parsed_rooms = {}
        self._parse_sheet(gspread_sheet, room_name_column, sheet_columns_mapping, room_name_to_svg_id)

    def get_parsed_rooms(self):
        return self._parsed_rooms

    
    def __eq__(self, other_parsed_sheet):
        """ This lets us use `sheet_one != sheet_two` to check if there has been a change in the sheets """
        if other_parsed_sheet is None:
            return False
        if not isinstance(other_parsed_sheet, RoomDataParser):
            raise Exception("Cannot call == on a RoomDataParser and a non-RoomDataParser")
        
        other_parsed_rooms = other_parsed_sheet.get_parsed_rooms()
        num_other_rooms = len(other_parsed_rooms)
        num_this_rooms = len(self._parsed_rooms)

        # something has changed if number of rooms is different
        if num_other_rooms != num_this_rooms:
            return False

        # we might need to check all the values of attributes otherwise
        # could also do this with set opesrations over pairs/triples etc
        for room in self._parsed_rooms:
            if room not in other_parsed_rooms:
                return False

            room_attrs = self._parsed_rooms[room]
            other_room_attrs = other_parsed_rooms[room]

            # compare all attrs
            for attr, attr_value in room_attrs.items():
                if attr_value != other_room_attrs[attr]:
                    return False
        return True

    def __ne__(self, other_parsed_sheet):
        """ For python2 compatibility """
        return not self.__eq__(other_parsed_sheet)


    def _parse_sheet(self, gspread_sheet, name_column, columns_mapping, room_name_to_svg_id):

        for row in gspread_sheet.get_all_values():
            room_name = row[name_column]
            # skip all invalid room names/unknown room names
            if room_name not in room_name_to_svg_id:
                self._logger.log("Skipping room name `" + room_name + "`, not a (known or) valid room name, check mapping file")
                continue
            
            room_id = room_name_to_svg_id[room_name]
            room_attributes = self._parse_sheet_row_to_room_attributes(row, columns_mapping)
            self._parsed_rooms[room_id] = room_attributes # includes room name in here


    def _parse_sheet_row_to_room_attributes(self, row, columns_mapping):
        room_attributes = {}
        for attribute in columns_mapping:
            attribute_index = columns_mapping[attribute]

            # ignore attributes that have been given a -1 index, ie. ignore this attribute
            if attribute_index == -1:       # signal values to ignore
                # TODO remove this hardcoded attribute if allowed by the frontend requirements
                room_attributes[attribute] = ''      #but this attr may be hard coded in somewhere...
            else:
                room_attributes[attribute] = row[attribute_index]
        return room_attributes
