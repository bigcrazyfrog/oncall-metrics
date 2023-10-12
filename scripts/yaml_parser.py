# Script for automation of the duty process.

import requests
import yaml

from conf import PASSWORD, USER, YAML_FILE_PATH
from oncall import (add_user_to_team, create_event, create_team,
                           create_user, get_csrf_token)


if __name__ == "__main__":
    # Read yaml file
    yaml_file = yaml.load(open(YAML_FILE_PATH), Loader=yaml.CLoader)
    teams = yaml_file["teams"]

    with requests.Session() as session:
        # Add new auth csrf token to headers
        session.headers = {'X-CSRF-TOKEN': get_csrf_token(session, USER, PASSWORD)}

        for team in teams:
            # Create a new team
            create_team(session, team)

            for user in team.get("users", []):
                # Create new user
                create_user(session, user)

                # Add user to team
                add_user_to_team(session, user['name'], team['name'])

                for event in user.get("duty", []):
                    # Create new event
                    create_event(session, user["name"], team["name"], event)
