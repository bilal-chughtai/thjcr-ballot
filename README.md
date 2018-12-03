# thjcr-ballot
Everything needed to run the TH jcr ballot, minus the floor plans and the Google API private key.


## Usage

Clone this repository to a NON-PUBLIC location on your server. If using SRCF and your home directory is `home/xx123/`, this is as good a place as any. You will need access to the `thjcr` society if you plan on putting the ballot on the TH jcr website. In 2017, we were using `~/thjcr/public_html/Ballot-Viz/` to host the actual files.

You'll also need to get a copy of the annotated floor plans (SVG) from myself or the prior webmaster, as well as the Google API secret credentials (private key), and put them somewhere _NON-PUBLIC_ (regarding floor plans, I'm not sure if they can be public so this is just to play it safe).

-------

0. Clone this repository to a non-public directory, obtain the annotated floor plan SVGs, and the Google API secret.

1. Share the Google doc with `TODO`

2. Create a new ballot

Let's say we wish to create a ballot for 2019, and it should live under `~/thjcr/public_html/Ballot-Viz`. You have the floor plan SVGs under `~/balloting/plans/`, and the Google API secret `.json` under `~/balloting/google_api_secret.json`. Lets also assume the name of the google doc containing the balloting spreadsheet is "Ballot-Room-Document-2017.xlsx" Then execute:

```
python3 -m create_ballot 
    --year 2019 
    --output-directory ~/thjcr/public_html/Ballot-Viz
    --google-API-credentials ~/balloting/google_api_secret.json
    --google-doc-title "Ballot-Room-Document-2017.xlsx" 
    --floor-plan-svgs-directory ~/balloting/plans/
```

3. Run the server to update the ballot when it needs to be update on the fly