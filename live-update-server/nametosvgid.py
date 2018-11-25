class RoomNameToSvgId():
    """ Maps a room name from the Google Sheet to an SVG id - reverse of what's stored in the CSV """
    def __init__(self, svg_id_to_room_name_filepath):

        self._room_name_to_svg_id = {}
        with open(svg_id_to_room_name_filepath) as mapping_file:
            for mapping in mapping_file:
                (svg_id, room_name) = mapping.split(',')
                svg_id, room_name = svg_id.strip(), room_name.strip()
                self._room_name_to_svg_id[room_name] = svg_id

    def get_all_room_names(self):
        return self._room_name_to_svg_id.keys()
    
    def names_to_ids(self):
        return self._room_name_to_svg_id