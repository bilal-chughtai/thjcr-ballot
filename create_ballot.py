import os
import argparse
import shutil

from app.gsheet_tools.googlesheet import GoogleSheetReader

parser = argparse.ArgumentParser(
    description="Create a copy of the ballot into a specified location. The files may then be updated by executing `gsheet_tools/server.py`, ")
parser.add_argument("--ballot-directory", required=True,
                    help="Path to currently active ballot where this script has write permissions", type=str)
parser.add_argument("--google-API-credentials", required=True,
                    help="Path to JSON file with the Google Drive API secret (aka credentials) that authorizes access google sheets that have been shared to the account",
                    type=str)
parser.add_argument("--no-delete-existing", dest="delete_existing", action="store_false",
                    help="Don't delete existing ballot directory if present already")
parser.add_argument("--delete-existing", dest="delete_existing", action="store_true",
                    help="(default) delete existing ballot directory if present")
parser.set_defaults(delete_existing=True)
parser.add_argument("--floor-plan-svgs-directory", required=True,
                    help="Where to find all the SVGs to find required for the site - this isn't bundled with the Git repository because unsure whether these floorplans should be public. On the SRCF server place them somewhere non-public and in the ballot-site use a .htaccess to restrict access (default settings will be copied).")
parser.add_argument("--google-doc-title", required=True,
                    help="Exact name of the google doc to link the ballot site to.")


def copy_and_update_index_file(source, dest, key):
    fIn = open(source)
    fOut = open(os.path.join(dest, 'index.html'), "w")
    for line in fIn:
        if "REPLACE_THIS_WITH_KEY" in line:
            line = line.replace("REPLACE_THIS_WITH_KEY", key)
        fOut.write(line)
    fIn.close()
    fOut.close()


def delete_directory(pathstring):
    try:
        shutil.rmtree(pathstring)
        print("\nDeleted {0}".format(pathstring))
    except FileNotFoundError as e:
        print("\nSkipping deletion, directory {0} does not exist".format(pathstring))


args = parser.parse_args()
ballot_directory = args.ballot_directory

sheet_reader = GoogleSheetReader(args.google_API_credentials)
google_doc_id = sheet_reader.get_doc_id(args.google_doc_title.strip())

# delete existing files if required
delete_existing = args.delete_existing
if delete_existing:
    delete_directory(ballot_directory)

# create directory if not already there
# then copy files over
try:
    os.mkdir(ballot_directory)
    shutil.copy("site_template/style.css", ballot_directory)
    shutil.copy("site_template/svgStyling.css", ballot_directory)
    print("Successfully copied styles to {0}".format(ballot_directory))
    shutil.copytree("site_template/res", os.path.join(ballot_directory, "res"))
    print("Successfully copied resources to {0}".format(os.path.join(ballot_directory, "res")))
    shutil.copy("site_template/scripts_new.js", ballot_directory)
    print("Successfully copied scripts to {0}".format(ballot_directory))
    shutil.copy("site_template/.htaccess", ballot_directory)
    print("Successfully copied htaccess to {0}".format(ballot_directory))
    copy_and_update_index_file("site_template/index.html", ballot_directory, google_doc_id)
    print("Successfully copied & updated index to {0}".format(ballot_directory))
    # target folder of target/plans may not exist before
    shutil.copytree(args.floor_plan_svgs_directory, os.path.join(ballot_directory, "plans"))
    print("Successfully copied floor plans to {0}".format(os.path.join(ballot_directory, "plans")))
except Exception as e:
    # directory exist/error with file copying
    print(e)
    pass

print(
    "\n\n***** You now need to run `gsheet_tools/server.py` pointing to the created directory `{0}` to get live updates on it *****".format(
        ballot_directory))
print("""Partial command:\n \
python3 -m gsheet_tools.server \
--ballot-directory "{0}" \
--google-API-credentials "{1}" \
--google-doc-title "{2}" \
--google-sheet-name [SHEETNAME] \
--google-sheet-format [FORMAT FILE] \
--room-svg-id-mapping [MAPPING FILE]""".format(
    ballot_directory,
    args.google_API_credentials,
    args.google_doc_title.strip()
))
