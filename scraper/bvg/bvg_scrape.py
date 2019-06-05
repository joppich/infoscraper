#!/usr/bin/env python3

import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

basepath = os.path.dirname(__file__)


class BvgScraper:

    results = {}
    
    def __init__(self):
        with open(os.path.join(basepath,"url.txt"),"r") as _f:
            url_template = _f.read()
        url = url_template.format(CURRENT_TIME=datetime.strftime(datetime.now(), "%H:%M"))
        raw = requests.get(url)
        plain = raw.text
        self.parsed = BeautifulSoup(plain, "html.parser")
        self._parse_departures()

    def _parse_departures(self):
        self.results.update(dict(departures=[]))
        dep_table = self.parsed.find_all("table")[0]
        deps = [x for x in dep_table.find_all("tr")[2:] if x and x != -1]

        for row in deps:
            result_entry = {}
            a_list = [i.get_text().strip() for i in row.find_all("a")]
            for a in a_list:
                if a.startswith("Bus") or a.startswith("U3"):
                    result_entry.update(dict(line=a))
                else:
                    result_entry.update(dict(terminus=a))
            dep_time = row.find("span").get_text().strip()
            result_entry.update(dict(time=dep_time))
            self.results["departures"].append(result_entry)

    def json(self):
        return json.dumps(self.results, ensure_ascii=False)


if __name__ == "__main__":
    scraper = BvgScraper()
    print(scraper.json())
