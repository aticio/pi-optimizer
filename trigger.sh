#!/bin/bash
cp -rp /opt/tickrecorder/tickrecorder.db /tmp/
sqlite3 -csv /tmp/tickrecorder.db "select * from tick_price;" > /tmp/tickrecorder.csv
cd /opt/pi/
pip install -r requirements.txt -U
nohup python3 /opt/pi-optimizer/pi-optimizer.py > /dev/null 2> /dev/null < /dev/null &