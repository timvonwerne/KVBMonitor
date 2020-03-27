# KVB Monitor
The aim of this project is to display departures to a LED RGB matrix.

Credits for rgbmatrix library: https://github.com/hzeller/rpi-rgb-led-matrix

## Installation/ Activation
1. `apt-get install libjpeg9-dev`
2. `source bin/activate`
3. To install all of the requirements enter: `pip install -r requirements.txt`.
4. To run the script, enter: `sudo bin/python kvbmonitor.py`

Note: root privileges required due to LED matrix.

## Service
In order to activate the service and run it on every restart, execute:
1. `sudo chmod +x service/matrix.sh` to make the service executable.
2. `sudo systemctl enable /home/pi/KVBMonitor/service/kvbmonitor.service` to enable the daemon.

Any flags for configuring the matrix such as number of rows, number of columns, brightness etc. can be adjusted in `service/matrix.sh`.