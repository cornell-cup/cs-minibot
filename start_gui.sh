#!/bin/bash

echo "================= MINIBOT GUI ================="
cd gui
npm run webpack
echo "=========== WEBPACK SETUP COMPLETE ============"
PYTHONPATH=.. python3 main.py &
echo "============== GUI SETUP COMPLETE ============="
echo "GUI is now running! Go to localhost:8080 to view the GUI."