#!/usr/bin/env python3

import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

basepath = os.path.dirname(__file__)

weekdays_ger = ["montag","dienstag","mittwoch","donnerstag","freitag","samstag","sonntag"]


class FoodScraper:

    results = {}
   
    def _get_dow(self):
        return weekdays_ger[datetime.today().weekday()]

    def __init__(self):
        with open(os.path.join(basepath,"url.txt"),"r") as _f:
            url_template = _f.read()
        url = url_template.format(DOW=self._get_dow()).strip()
        raw = requests.get(url)
        plain = raw.text
        self.parsed = BeautifulSoup(plain, "html.parser")
        self._parse_food()

    def _parse_food(self):
        food_classes = self.parsed.find_all("div", class_ = "aw-meal-category")
        self.results.update({x.find("h3").text : [y.text for y in x.find_all("p", class_ = "aw-meal-description")] \
                for x in food_classes})
        del self.results["Salate"]

    def json(self):
        return json.dumps(self.results, ensure_ascii=False)


if __name__ == "__main__":
    scraper = FoodScraper()
    print(scraper.json())
