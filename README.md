# thjcr-ballot
Everything needed to run the Trinity Hall JCR ballot visualization, minus the floor plans and the Google API private key. Contact me or previous webmasters for them.


## Usage

Clone this repository to a NON-PUBLIC location on your server. If using SRCF and your home directory is `home/xx123/`, this is as good a place as any. You will need access to the `thjcr` society if you plan on putting the ballot on the Trinity Hall JCR website. In 2017, we were using `~/thjcr/public_html/Ballot-Viz/` to host the files for this system.

You'll also need to get a copy of the annotated floor plans (SVG) from myself or the prior webmaster, as well as the Google API secret credentials (private key), and put them somewhere _NON-PUBLIC_ (regarding floor plans, I'm not sure if they can be public, so this is just to play it safe). You may be able to find these private files on the SRCF server from the prior year. *Also change the permissions of the folder containing these documents so that only members of thjcr can read the folder*.

1. Clone this repository to a non-public directory, obtain the annotated floor plan SVGs, and the Google API secret. Also install `gspread` and `oauth2client`: `pip3 install gspread oauth2client`

2. Share the ballot document google sheet with `gdoc-editor@thjcr-ballot-system.iam.gserviceaccount.com`, which gives this system access to the google doc.

3. Create a new ballot:

Let's say we wish to create a ballot for 2019, and it should live under `~/thjcr/public_html/Ballot-Viz/`. You have the floor plan SVGs under `~/balloting/plans/`, and the Google API secret `.json` under `~/balloting/google_api_secret.json`. Lets also assume the name of the google doc containing the balloting spreadsheet is "Copy of Ballot-Room-Document-2017.xlsx".
Then execute:

```
python3 -m create_ballot 
    --ballot-directory ~/thjcr/public_html/Ballot-Viz/2019
    --google-API-credentials ~/balloting/google_api_secret.json
    --google-doc-title "Copy of Ballot-Room-Document-2017.xlsx" 
    --floor-plan-svgs-directory ~/balloting/plans/
```

4. Run the server to generate live updates. You probably only need to leave this running couple days/weeks the ballot is actually being changed. (See next section `"Tmux"` on how to do this best).

To get the live-updates, this time we also need to provide the specific sheet of the google sheet to read from,
and specify which columns to read from with the `--sheet-format` parameter, and the mapping from room names in the Google Sheet 
to the ID of the room in the floor plan SVG files using the `--room-svg-id-to-room-name` parameter


```
python3 -m live_update_server.server
    --ballot-directory ~/thjcr/public_html/Ballot-Viz/2019
    --google-API-credentials ~/balloting/google_api_secret.json
    --google-doc-title "Copy of Ballot-Room-Document-2017.xlsx"
    --google-sheet-name "somesheet"
    --google-sheet-format live_update_server/resources/google-sheet-format.json
    --room-svg-id-mapping live_update_server/resources/room_id_mapping.csv
```

### Tmux for live update server
You'll need to use `screen` or `tmux` to leave the live update server running while you're not logged in.
I recommend `tmux`, especially since its available on the SRCF server as well.

Basic usage you'll need

1. Log into server, navigate to this directory, and create the ballot if it doesn't already exist.
2. Start tmux. You can use `tmux new -s ballot2019`
3. Once inside the tmux session, run the command from Step 4 in the prior section
4. Detach from tmux (this will essentially leave it running in the background) by pressing the `CTRL + d` key combination.
5. You can now log out of the server if you want.

To go back and shut down the server
1. Log into server
2. Re-attach to the tmux session: `tmux a -t ballot2019`
3. Kill the server (`CTRL + c`)
4. Kill the tmux session: `tmux kill-session`
5. Log out of the sever if you want.

## Development

This repo is pretty easy to develop on top of. Use your favourite IDE (I use PyCharm), and set up a virtual environment using Python 3.4. In a JetBrains IDE this is done via File > Settings > Project > Project Interpreter > [Cog Icon] > Ok. Then pip install requirements.txt and you should be able to run the above commands locally.

Current planned additions:  
Retain google sheet infrastructure as it's "easy" in case we get a naff webmaster some year  
Add reading in of sheet containing timings  
figure out how to user expose an authenticated to select rooms in time slot and push these changes to the master sheet  
probably keep the reader (+visualiser) and writer processes seperate 
use django framework to user expose 

