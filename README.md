# Data-Upload-Service

A simple system to exploit experimental data.

This was just a small POC . 

The current development is being done as part of 3 projects (PhysMET, MATCHMAKER , PINK), it is available here: https://github.com/EMMC-ASBL/datadocweb

## Current Functionality

Currently it takes in an Excel sheet and populates the GraphDB in the backend.
Backend can be changed.
Currently using : http://10.218.121.139:7200/repositories/MatCHMaker   (you need to be on the SINTEF network to access it )

## Tested with SIMAVI Graph
You can comment out the SINTEF graph urls (Line 17-18) and uncomment the simavi graph urls (Line 21-22) in main.py file
You need to be connected to SIMAVI VPN
http://10.222.30.203:7200/graphs

## Running the service

`docker-compose up --build -d`


