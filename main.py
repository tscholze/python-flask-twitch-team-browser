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
        return render_template("index.html",team_name=team_name, include_mature=include_mature, team=get_team_by_name(team_name, include_mature))
    else:
        return render_template("index.html")

def get_team_by_name(team_name, include_mature):
    # Configurate request header
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': configuration.TWITCH_CLIENT_ID 
    }

    # Build url with entered team name
    # TODO: Encode team name to http save chars.
    url = configuration.TWITCH_TEAMS_BASE_ENDPOINT_URL + "/" + team_name

    # Send request and try to parse response as json.
    response = requests.get(url, headers=headers).json()

    print(response)

    # Check if mature members should be included.
    if include_mature == False:
        response["users"] = filter(lambda member: member["mature"] == False, response["users"])

    return response


if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)