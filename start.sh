#!/bin/bash

python3 app.py &

sleep 2

ngrok http 8080
