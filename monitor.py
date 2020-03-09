from bs4 import BeautifulSoup
from datetime import datetime
import requests
import threading
from parse import *

STATION_ID = 632

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
}

def get_departures():
    threading.Timer(30.0, get_departures).start()
    url = "https://kvb.koeln/qr/%d/" % STATION_ID
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text)
    tables = soup.find_all("table", class_="display")
    departures = []
    for row in tables[0].find_all("tr"):
        tds = row.find_all("td")
        (line_id, direction, time) = (tds[0].text, tds[1].text, tds[2].text)
        line_id = line_id.replace(u"\xa0", "")
        direction = direction.replace(u"\xa0", "")
        time = time.replace(u"\xa0", "").strip().lower()
        if time == "sofort":
            time = "0"
        time = time.replace(" min", "")
        try:
            time = int(time)
        except:
            pass
        try:
            line_id = int(line_id)
        except:
            pass
        if (direction == "Rochusplatz") or (direction == "Bocklemünd"):
            departures.append({
                "line_id": line_id,
                "direction": direction,
                "wait_time": time
            })
    departuresCount = len(departures)
    print(departuresCount)
    for i in range(0, departuresCount):
        print("%a  %b  %c  \n" % (departures[i]['line_id'], departures[i]['direction'], departures[i]['wait_time']))
    
get_departures()