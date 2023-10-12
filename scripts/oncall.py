import datetime
import logging
import time
from typing import Any, Final

import requests
from conf import BASE_URL

# This module contains methods to interact with Oncall API
# https://oncall.tools/docs/api.html

# One day in timestamp format
TIMESTAMP_DAY: Final = 86400.0


def get_csrf_token(session: requests.Session, username: str, password: str) -> str:
    """Get csrf authentication token."""
    auth_data = {
        "username": username,
        "password": password,
    }
    response = session.post(f"{BASE_URL}/login", data=auth_data)
    response.raise_for_status()
    return response.json().get("csrf_token")


def create_team(session: requests.Session, team: dict[str, Any]) -> None:
    """Create a new team."""
    team_creation_url = f"{BASE_URL}/api/v0/teams/"
    team_json = {
        "name": team.get("name"),
        "scheduling_timezone": team.get("scheduling_timezone"),
        "email": team.get("email"),
        "slack_channel": team.get("slack_channel"),
        "slack_channel_notifications": team.get("slack_channel_notifications"),
        "admin": team.get("admin"),
    }

    response = session.post(team_creation_url, json=team_json)
    logging.info(f"{response.status_code} Add team {team['name']}")


def create_user(session: requests.Session, user: dict[str, Any]) -> None:
    """Create a new user."""
    user_creation_url = f"{BASE_URL}/api/v0/users/"
    user_creation_json = {"name": user["name"]}
    response = session.post(user_creation_url, json=user_creation_json)
    logging.info(f"{response.status_code} Add user {user['name']}")

    # Update user info
    user_update_url = f"{BASE_URL}/api/v0/users/{user['name']}"
    user_update_json = {
        "contacts": {
            "call": user.get("phone_number"),
            "email": user.get("email"),
        },
        "full_name": user.get("full_name"),
    }
    response = session.put(user_update_url, json=user_update_json)
    logging.info(f"{response.status_code} Edit user {user['name']}")


def add_user_to_team(session: requests.Session, username: str, team_name: str) -> None:
    """Add user to team.

    Args:
        session: Current session for request.
        username: Username for the user.
        team_name: Name for the team.

    """
    team_user_url = f"{BASE_URL}/api/v0/teams/{team_name}/users"
    team_user_json = {
        "name": username,
    }
    response = session.post(team_user_url, json=team_user_json)
    logging.info(f"{response.status_code} Add user {username} to team {team_name}")


def create_event(
    session: requests.Session,
    username: str,
    team_name: str,
    event: dict[str, Any],
) -> None:
    """Create a new event.

    Args:
        session: Current session for request.
        username: Username for the event's user.
        team_name: Name for the event's team.
        event: Event info, it should contain `date` and `role` field.

    """
    event_creation_url = f"{BASE_URL}/api/v0/events"
    start = time.mktime(datetime.datetime.strptime(event["date"], "%d/%m/%Y").timetuple())
    event_json = {
        "start": start,
        "end": start + TIMESTAMP_DAY,
        "user": username,
        "team": team_name,
        "role": event["role"],
    }
    response = session.post(event_creation_url, json=event_json)
    logging.info(f"{response.status_code} Add duty for {username} on {event['date']}")
