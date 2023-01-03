from datetime import datetime
from enum import auto
import requests
from strenum import StrEnum
import pygsheets
import time


WAIT = 10


class GymEnum(StrEnum):
    BROOKLYN = auto()


SAFE_SPACE_CODES = {
    GymEnum.BROOKLYN: "a7796f34",
}


def build_url(gym_identifier: GymEnum) -> str:
    return f"https://display.safespace.io/value/live/{SAFE_SPACE_CODES.get(gym_identifier)}"


def fetch_current(gym_identifier: GymEnum) -> int:
    resp = requests.get(build_url(gym_identifier))
    if resp.status_code != 200:
        raise Exception(
            f"Failed to fetch current occupancy for {gym_identifier.value}: {resp.status_code} {resp.text}"
        )

    return int(resp.json())


def write_to_sheet(gym_identifier: GymEnum, curr_occ: int):
    gc = pygsheets.authorize(service_file="credentials.json")
    sh = gc.open("Vital Tracker")
    wks = sh[0]
    wks.insert_rows(
        wks.rows,
        values=[
            datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            gym_identifier.value,
            curr_occ,
        ],
        inherit=True,
    )


def run():
    gym = GymEnum.BROOKLYN
    curr = fetch_current(gym)
    print(gym, curr)
    write_to_sheet(gym, curr)


if __name__ == "__main__":
    while True:
        run()
        time.sleep(WAIT)
