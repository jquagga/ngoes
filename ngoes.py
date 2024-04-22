#!/usr/bin/env python

"""upa.py: microplane alert. Checks sdr ultrafeeder output
for interesting planes and issues notifications."""

import datetime
import json
import os
import time

import apprise
import requests


def notify(plane):
    print("hi")


def main():
    # First we set the location to poll based on NGOES_LOCATIONID variable
    # It defaults to El Paso since they usually have apts and are great for testing code!
    location_id = os.environ.get("NGOES_LOCATIONID", "5005")
    json_url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId={location_id}&minimum=1"

    notify_url = notify_url = os.environ.get(
        "NGOES_NOTIFY_URL", "ntfy://ngoesunconfigured/?priority=min"
    )

    # We're going to keep a local list of times to keep from reporting times over and over again
    # It is reset if the program restarts so that restarts the reporting clock
    reported_times = []
    while 1:
        print("Polling appointments")
        # Poll URL and load in the json
        response = requests.get(json_url, timeout=5)
        json = response.json()
        # Did we get anything back, if not, no appointments found.
        if not json:
            print("No Appointments Found")
        else:
            two_weeks_future = time.time() + 1209600
            # If we did get something back, lets loop through results
            for appointment in json:
                # appointment_str is human readable
                # appointment_timestamp is a numeric timestamp we will use
                # to check if appointment is in the next 2 weeks
                appointment_str = appointment["startTimestamp"]
                appointment_timestamp = datetime.datetime.strptime(
                    appointment["startTimestamp"], "%Y-%m-%dT%H:%M"
                ).timestamp()

                # First is this appointment less than 2 weeks in the future?
                if appointment_timestamp < two_weeks_future:
                    # And then, is it also an appointment we haven't reported yet?
                    if appointment_timestamp not in reported_times:
                        reported_times.append(appointment_timestamp)

                        notification = f"A Global Entry appointment is available at {appointment_str}"
                        print(notification)

                        apobj = apprise.Apprise()
                        apobj.add(notify_url)
                        apobj.notify(
                            body=notification,
                        )

        print("Sleeping 15 minutes")
        time.sleep(900)


if __name__ == "__main__":
    main()
