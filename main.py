from flask import Flask, render_template, request
import configuration
import requests

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    # If request is Post, request data from server.
    if request.method == "POST":
        # Get information from POST request.
        team_name = request.form.get("team_name")
        include_mature = True if request.form.get("include_mature") else False

        # Team name has to be set, otherwise return default page.
        if team_name is None:
            # TODO: Return error string to inform the user
            return "Error"

        # Return template with requested results.
        return render_template("index.html", results=get_team_members(team_name, include_mature))
    else:
        return render_template("index.html")

def get_team_members(team_name, include_mature):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': configuration.TWITCH_CLIENT_ID 
    }
    url = configuration.TWITCH_TEAMS_BASE_ENDPOINT_URL + "/" + team_name
    members = requests.get(url, headers=headers).json()["users"]

    if include_mature == False:
        members = filter(lambda member: member["mature"] == False, members)

    return members


if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)