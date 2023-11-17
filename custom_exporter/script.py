from prometheus_client import start_http_server, Gauge, Summary, Info
import random
import time
from time import sleep
import requests

HOST = "oncall:8080"


def count_teams():
    return len(requests.get(f"http://{HOST}/api/v0/teams").json())


def count_users():
    return len(requests.get(f"http://{HOST}/api/v0/users").json())


def is_event_today():
    time_now = int(time.time())
    return int(len(requests.get(f"http://{HOST}/api/v0/events?start__le={time_now}").json()) > 0)
    

if __name__ == '__main__':
    number_of_teams = Gauge('number_of_teams', 'Number of teams gauge')
    number_of_users = Gauge('number_of_users', 'Number of users gauge')
    event_today = Gauge('is_event_today', 'is event today')
    
    # Start up the server to expose the metrics.
    start_http_server(8082)
    # Generate some requests.
    while True:
        try:
            number_of_teams.set(count_teams())
            number_of_users.set(count_users())
            event_today.set(is_event_today())
        except:
            sleep(1)
