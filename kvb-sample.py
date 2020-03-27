#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import datetime
import schedule
from bs4 import BeautifulSoup
import requests
import threading

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("resources/fonts/5x8.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
        }
        
        url = "https://kvb.koeln/qr/632/"

        while True:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, features="html.parser")
            tables = soup.find_all("table", class_="display")
            departures = []
            for row in tables[0].find_all("tr"):
                tds = row.find_all("td")
                (line_id, direction, wait_time) = (tds[0].text, tds[1].text, tds[2].text)
                line_id = line_id.replace(u"\xa0", "")
                direction = direction.replace(u"\xa0", "")
                wait_time = wait_time.replace(u" Min", "m").strip()
                try:
                    line_id = int(line_id)
                except:
                    pass
                if(direction == "Bocklemünd" or direction == "Rochusplatz"):
                    departures.append({
                        "line_id": line_id,
                        "direction": direction,
                        "wait_time": wait_time
                    })
                    
            offscreen_canvas.Clear()

            # Display the current date and time on top
            now = datetime.datetime.now()
            curr_date = now.strftime("%d.%m.%Y")
            curr_time = now.strftime("%H:%M")
            graphics.DrawText(offscreen_canvas, font, 3, 2, textColor, curr_date)
            graphics.DrawText(offscreen_canvas, font, 36, 2, textColor, curr_time)
            
            # Set y-position of first connection to 16px
            ymargin = 16

            print("{0}        {1}".format(curr_date, curr_time))

            for depart in departures:
                if(depart['direction'] == "Bocklemünd"): depart['direction'] = "Bockl."
                if(depart['direction'] == "Rochusplatz"): depart['direction'] = "Rochu."
                connection = "{0} {1} {2}".format(str(depart['line_id']), depart['direction'], depart['wait_time'])    
                print(connection)
                graphics.DrawText(offscreen_canvas, font, 2, ymargin, textColor, connection)
                ymargin = ymargin + 10

            time.sleep(30)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()