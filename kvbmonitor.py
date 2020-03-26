import schedule
import time
from bs4 import BeautifulSoup
import requests
import threading
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

STATION_ID = '632'
MATRIX_COLS = 32
MATRIX_ROWS = 64

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
}

options = RGBMatrixOptions()
options.rows = MATRIX_ROWS
options.cols = MATRIX_COLS
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)

canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("resources/fonts/4x6.bdf")
textColor = graphics.Color(255, 255, 0)
pos = canvas.width

def get_departures():
    url = "https://kvb.koeln/qr/%d/" % int(STATION_ID)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="html.parser")
    tables = soup.find_all("table", class_="display")
    departures = []
    for row in tables[0].find_all("tr"):
        tds = row.find_all("td")
        (line_id, direction, time) = (tds[0].text, tds[1].text, tds[2].text)
        line_id = line_id.replace(u"\xa0", "")
        direction = direction.replace(u"\xa0", "")
        time = time.replace(u"\xa0", " ").strip().lower()
        try:
            line_id = int(line_id)
        except:
            pass
        if(direction == "Bocklemünd" or direction == "Rochusplatz"):
            departures.append({
                "line_id": line_id,
                "direction": direction,
                "wait_time": time
            })
    return departures

def print_departures_to_matrix():
    canvas.Clear()
    lines = []
    for d in get_departures():
        line = "{0}    {1}    {2}".format(str(d['line_id']), d['direction'], d['wait_time'])
        print(line)
        graphics.DrawText(canvas, font, pos, 10, textColor, line)


print_departures_to_matrix()
schedule.every(10).seconds.do(print_departures_to_matrix)

while 1:
    schedule.run_pending()
    time.sleep(1)
    