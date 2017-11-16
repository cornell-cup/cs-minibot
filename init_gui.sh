#!/bin/bash

echo "=============== MINIBOT GUI SETUP ================"
pip install -r requirements.txt
cd gui
npm install
npm run webpack
echo "================= SETUP COMPLETE ================="
