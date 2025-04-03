import requests
from bs4 import BeautifulSoup

from typing import Union

url = "https://www.bjjheroes.com/a-z-bjj-fighters-list"


# Figure out how to store this data before putting it in a database


class Collection:
    def __init__(self, url) -> None:
        self.url = url

    def fetch_data(self, url) -> Union[BeautifulSoup, None]:
        response = requests.get(url)
        response.encoding = "utf-8"  # Set the correct encoding
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    def get_athlete_link(self) -> list[str]:
        soup = self.fetch_data(self.url)
        if not soup:
            return {}

        athlete_links = []
        table = soup.find("table")  # Locate the table
        if not table:
            print("Data table not found.")

        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")

            first_name = cols[0].get_text(strip=True)
            last_name = cols[1].get_text(strip=True)
            full_name = first_name + " " + last_name
            team = cols[3].get_text(strip=True)

            first_name_tag = cols[0].find("a")
            href = first_name_tag.get("href")
            athlete_link = self.url + href

            athlete_links.append(athlete_link)

        return athlete_links

    def get_athlete_fight_history(self) -> dict[str, str]:
        athlete_directory = self.get_athlete_link()

        fight_history_all = {}
        for athlete in athlete_directory[:10]:
            soup = self.fetch_data(athlete)
            if not soup:
                return {}

            table = soup.find("table")  # Locate the table
            if not table:
                print(f"Data table not found: {athlete}")
                continue

            rows = table.find_all("tr")[1:]  # Skip the header row

            athlete_fights = []
            try:
                for row in rows:
                    cols = row.find_all("td")

                    if len(cols) < 8:
                        continue

                    opponent_span = cols[1].find("span")

                    opponent = (
                        opponent_span.get_text(strip=True) if opponent_span else "N/A"
                    )

                    win_loss = cols[2].get_text(strip=True)

                    method = cols[3].get_text(strip=True)

                    competition = cols[4].get_text(strip=True)

                    weight = cols[5].get_text(strip=True)

                    stage = cols[6].get_text(strip=True)

                    year = cols[7].get_text(strip=True)

                    athlete_fights.append(
                        {
                            "Opponent": opponent,
                            "Record": win_loss,
                            "Method": method,
                            "Competition": competition,
                            "Weight": weight,
                            "Stage": stage,
                            "Year": year,
                        }
                    )
                fight_history_all[athlete] = athlete_fights

            except Exception as e:
                # print(f"Athlete {athlete} had an error: {e}")
                continue
        return fight_history_all


def main(url: str) -> None:
    file = Collection(url)

    athletes = file.get_athlete_fight_history()

    print(athletes)


main(url)
