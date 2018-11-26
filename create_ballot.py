import os
import argparse
import shutil

from live_update_server.googlesheet import GoogleSheetReader

parser = argparse.ArgumentParser(description="Create an copy of the ballot, which can be updated by `server.py`")
parser.add_argument("--year", required=True, help="The year of the ballot being run (becomes folder name", type=int)
parser.add_argument("--output-directory", required=True, help="Where to create ballot directory and copy files into (on SRCF, this will be something like thjcr/Ballot-Viz/). With the new code structure as of late 2018, we no longer need to store all the code & ballot files in the same place, so thjcr/Ballot-Viz directory can have just 2018, 2019...")
parser.add_argument("--google-API-credentials", required=True, help="Path to JSON file with the Google Drive API secret (aka credentials) that authorizes access google sheets that have been shared to the account", type=str)
parser.add_argument("--no-delete-existing", dest="delete_existing", action="store_false")
parser.add_argument("--delete-existing", dest="delete_existing", action="store_true")
parser.set_defaults(delete_existing=True)



def copyAndUpdateIndexFile(dest, key):
	fIn = open("template/index.html")
	fOut = open(os.path.join(dest, 'index.html'), "w")
	for line in fIn:
		if "REPLACE_THIS_WITH_KEY" in line:
			line = line.replace("REPLACE_THIS_WITH_KEY", key)
		fOut.write(line)
	fIn.close()
	fOut.close()

def recursive_delete(pathstring):
    try:
		shutil.rmtree(pathstring)
    except Exception:
        pass

# TODO

args = parser.parse_args()
target_directory = os.path.join(args.output_directory, args.year)

delete_existing = args.delete_existing
if delete_existing:
    recursive_delete(target_directory)

sheet_reader = GoogleSheetReader(args.google_API_credentials, "dummysheetname")
google_doc_id = sheet_reader.get_doc_id()




print("***** You now need to run server.py pointing to the created directory to get live updates *****")