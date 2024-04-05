# Preface

This file contains the documentation of my process researching and implementing a database for the purpose of storing application and script output logs for usability on the frontend.

# Research and Installation

Currently, InfluxDB seems like a good option for our situation and is recommended by Dakota.

Server installation:
https://docs.influxdata.com/influxdb/v2/install/

Installed the ARM64 version on pi (automatically runs on startup!)

config file -> /etc/default/influxdb2

For installing the CLI:
https://docs.influxdata.com/influxdb/v2/tools/influx-cli/?t=Linux

Setup:
https://docs.influxdata.com/influxdb/v2/get-started/setup/?t=Set+up+with+the+CLI

USERNAME: PhoebusAdmin
PASSWORD: um~N:AgdY=r*bq3kS'x72@
ORG: PHOEBUS
BUCKET: Bucket_Main
RETENTION PERIOD: 24hrs

Tokens I generated for testing, NOT PRODUCTION!

Operator token: ZljwMMpff5DgJMLB3ruwnOA-F5N-3Ga6SiH1yNfbh4--Qquns2Q562m-2kldcTHk5Pk4uK_2vpO5nQxq1_Ft5Q==
All access token: Ta8xJFCts0uD0eipvNxQaAEdGZI6rJsX6V1o0RpJZExIxosejgANNRK6pMq--WPnL0j4iRzs5niWrjc0ikY9Tw==

Hosted on localhost:8086

Putting some example code in this directory for writing and querying the db!

