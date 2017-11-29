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