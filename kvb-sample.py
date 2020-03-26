#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import schedule
from bs4 import BeautifulSoup
import requests
import threading

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

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

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()