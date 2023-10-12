from datetime import date
from typing import Final
import os
import time
import requests
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

# Host and port of server
HOST: str = os.environ.get("HOST", "localhost")
PORT: str = os.environ.get("PORT", "8080")

# We use http because debug mode is assumed
BASE_URL: str = f"http://{HOST}:{PORT}"

# One day in timestamp format
TIMESTAMP_DAY: Final = 604800.0


def get_duty_team_list(date: float, role: str) -> list[str]:
    user_creation_url = f"{BASE_URL}/api/v0/events"
    params = {
        "start__ge": date,
        "end__le": date + TIMESTAMP_DAY,
        "role": role,
    }

    response = requests.get(user_creation_url, params=params)
    response.raise_for_status()

    return list(map(lambda duty: duty.get("team"), response.json()))


def get_team_list() -> list[str]:
    user_creation_url = f"{BASE_URL}/api/v0/teams"
    response = requests.get(user_creation_url)

    response.raise_for_status()
    return response.json()


def get_formatted_response() -> str:
    now_date = time.mktime(date.today().timetuple())

    teams = get_team_list()
    primary_duties = get_duty_team_list(now_date, "primary")
    secondary_duties = get_duty_team_list(now_date, "secondary")

    response = ""
    for team in teams:
        response += 'duty{team="%s", role="primary"} %s\n' % (team, int(team in primary_duties))
        response += 'duty{team="%s", role="secondary"} %s\n' % (team, int(team in secondary_duties))

    return response


app = FastAPI()


@app.get("/metrics")
def get_duty_metrics():
    try:
        return PlainTextResponse(get_formatted_response())
    except Exception as e:
        return PlainTextResponse(f"Oncall service is not available.", status_code=501)


if __name__ == "__main__":
    uvicorn.run("script:app", host="127.0.0.1", port=8090, workers=4)
