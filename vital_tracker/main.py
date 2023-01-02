from datetime import datetime
from enum import auto
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from strenum import StrEnum
from webdriver_manager.chrome import ChromeDriverManager
import pygsheets
import selenium.webdriver.chrome.webdriver
import time

WAIT = 60 * 10 # 10 minutes


class GymEnum(StrEnum):
    BROOKLYN = auto()


def build_url(gym_identifier: GymEnum) -> str:
    return f"https://www.vitalclimbinggym.com/{gym_identifier}".lower()


def fetch_current(
    driver: selenium.webdriver.chrome.webdriver.WebDriver, gym_identifier: GymEnum
) -> int:
    driver.get(build_url(gym_identifier))
    return int(driver.find_element(By.ID, "currocc").text)


def write_to_sheet(gym_identifier: GymEnum, curr_occ: int):
    gc = pygsheets.authorize(service_file="../credentials.json")
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


if __name__ == "__main__":
    chromedriver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    while True:
        gym = GymEnum.BROOKLYN
        curr = fetch_current(chromedriver, gym)
        print(gym, curr)
        write_to_sheet(gym, curr)
        time.sleep(WAIT)
