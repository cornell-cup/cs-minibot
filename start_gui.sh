#!/bin/bash

echo "================= MINIBOT GUI ================="
cd gui

if [ "$1" = "webpack" ]; then
    echo "Running webpack..."
    npm run webpack
    echo "=========== WEBPACK SETUP COMPLETE ============"
else
    echo "Skipping webpack..."
fi

PYTHONPATH=.. python3 main.py
echo "============== GUI SETUP COMPLETE ============="
echo "GUI is now running! Go to localhost:8080 to view the GUI."