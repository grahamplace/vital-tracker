from datetime import datetime
from enum import auto
from selenium.webdriver.common.by import By
from strenum import StrEnum
import pygsheets
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

WAIT = 60 * 10 # 10 minutes


class GymEnum(StrEnum):
    BROOKLYN = auto()


def build_url(gym_identifier: GymEnum) -> str:
    return f"https://www.vitalclimbinggym.com/{gym_identifier}".lower()


def fetch_current(
    driver, gym_identifier: GymEnum
) -> int:
    driver.get(build_url(gym_identifier))
    return int(driver.find_element(By.ID, "currocc").text)


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
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

    gym = GymEnum.BROOKLYN
    curr = fetch_current(driver, gym)
    print(gym, curr)
    write_to_sheet(gym, curr)
    driver.quit()


if __name__ == "__main__":
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    while True:
        gym = GymEnum.BROOKLYN
        curr = fetch_current(driver, gym)
        print(gym, curr)
        write_to_sheet(gym, curr)
        time.sleep(WAIT)
