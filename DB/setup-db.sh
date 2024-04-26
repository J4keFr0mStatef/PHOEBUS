# Update your package lists
sudo apt-get update

# Install InfluxDB server
wget https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_arm64.deb
sudo dpkg -i influxdb2_2.7.6-1_arm64.deb

# Start the InfluxDB service
sudo service influxdb start

# Install the InfluxDB CLI
wget https://download.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-arm64.tar.gz
tar xvzf ./influxdb2-client-2.7.5-linux-arm64.tar.gz
sudo cp ./influx /usr/local/bin/

# Remove the downloaded files
sudo rm influxdb2_2.7.6-1_arm64.deb
sudo rm influxdb2-client-2.7.5-linux-arm64.tar.gz