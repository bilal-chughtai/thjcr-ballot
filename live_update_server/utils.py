from datetime import datetime

def parse_gspread_date(date_string):
	return datetime.strptime(date_string[:19], '%Y-%m-%dT%H:%M:%S')

class NonRepeatingLogger():
    """ Logs messages with a count rather than repeating them. Writes to disk on every unseen message and periodically """
    def __init__(self, filepath, sort_by_most_recent=True):
        self._filepath = filepath
        self._messages = {}
        self._messages_elapsed_since_last_write = 0
        self._sort_by_most_recent = sort_by_most_recent

    def log(self, msg):
        if msg in self._messages:
            self._messages["count"] += 1
            self._messages["most_recent_timestamp"] = datetime.now()
            new_message = False
            self._messages_elapsed_since_last_write += 1
        else:
            print(msg)
            self._messages[msg] = {"count": 1, "most_recent_timestamp": datetime.now()}
            new_message = True

        self._write_log_if_needed(new_message)


    def _write_log_if_needed(self, new_message_in_log):
        if new_message_in_log or self._messages_elapsed_since_last_write > 100:
            self._write_log()
            self._messages_elapsed_since_last_write = 0

    def _write_log(self):
        logstrings = self._format_log()
        with open(self._filepath, "w") as logfile:
            for line in logstrings:
                logfile.write(line + "\n")

    def _format_log(self):
        messages = []
        for msg, msg_attrs in self._messages.items():
            msg_line = "{0}:\t{1}".format(msg_attrs["count"], msg)
            messages.append( (msg_line, msg_attrs["most_recent_timestamp"]))

        # sort messages by timestamp, ie. in increasing timestamp order
        if self._sort_by_most_recent:
            messages.sort(lambda pair: pair[1])

        # return only the messages themselves
        return [pair[0] for pair in messages]