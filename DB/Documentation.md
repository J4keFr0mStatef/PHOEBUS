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

Operator token: 0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw==
All access token: xkbWpVaw8_iOBi97aRSK-ILyLS-Yux2ifbG-qt6Q9VKw0TZeWUa8K0ngndro7Cf2xYy2Cm1V4Dtol6RXf6NYMA==

Hosted on localhost:8086

Putting some example code in this directory for writing and querying the db!