#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from urllib.parse import quote
import requests

# POST http header.
# Edit or change key.
POST_HEADER = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': "tfs0skg1ggojjik59kfv7rnqs3myq7"
}

# Webapp's root object.
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Route for GET and POST index / browsing request.
    It will render a template for presenting an overview
    of team members with additional information.

    :return: Index template with or without properties.
    """

    # If request is POST, reponse requested data.
    if request.method == "POST":
        # Get information from POST request.
        team_name = request.form.get("team_name").lower()
        include_mature = True if request.form.get("include_mature") else False

        # Team name has to be set, otherwise return default page.
        if team_name is None or team_name is "":
            return render_template("index.html", team=None)

        # Return template with requested results.
        return render_template("index.html", team_name=team_name, include_mature=include_mature, team=get_team_by_name(team_name, include_mature))
    else:
        # If request is a GET,  response with no team set (intial request of user).
        return render_template("index.html", team=None)


def get_team_by_name(team_name, include_mature):
    """
    Gets a team object from the Twitch API by given name.
    Filters mature tagged content out if `include_mature` if False.
    It will enrich the data with additional information such as online status.

    :param team_name: Name of the team to look for.
    :param include_mature: If True, the return value will include as mature tagged streamers.
    :return: Enriched team object from API.
    """

    # Build url with entered team name
    url = "https://api.twitch.tv/kraken/teams/" + quote(team_name)

    # Send request and try to parse response as json.
    response = requests.get(url, headers=POST_HEADER).json()

    # If response contains no users, return.
    if "users" not in response:
        return response

    # Check if mature members should be included.
    if include_mature == False:
        response["users"] = list(
            filter(lambda member: member["mature"] == False, response["users"]))

    # Enrich online information to response
    response = get_online_status_of_team_members(response)

    # Sort by online status
    response["users"].sort(
        key=lambda member: member["is_online"], reverse=True)

    return response


def get_online_status_of_team_members(team_response):
    """
    Gets the online status of team members.
    It will enrich the given team object with parsed data.

    :param team_reponse: Underlying team object from prior requests.
    :return: With online status enriched team object.
    """

    # Loop / map  over all members to build parameter string
    # Like: ?user_id=123&user_id=456&user_id=789
    parameter = "?"
    for member in team_response["users"]:
        parameter = parameter + f"user_id={member['_id']}&"

    # Build url with mapped member ids
    url = "https://api.twitch.tv/helix/streams" + parameter

    # Send request and try to parse response as json.
    response = requests.get(url, headers=POST_HEADER).json()

    # Extract user_ids from response as users that are currently
    # online.
    online_member_ids = list(
        map(lambda member: member["user_id"], response["data"]))

    # Loop over all members and check if member's user_id is included
    # in the responded online id list. Set True or False to the
    # `is_online` prorperty.``
    for member in team_response["users"]:

        if member["_id"] in online_member_ids:
            member["is_online"] = True
        else:
            member["is_online"] = False

    # Return enriched team object.
    return team_response


# Entry point.
if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
