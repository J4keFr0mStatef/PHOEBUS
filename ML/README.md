# Setting up the ML directory on the Raspberry Pi

1. Navigate to the ML installation directory.
   ```bash
   cd ~/ML/installation
   ```
2. Execute the setup-ML.sh script. __Do not use sudo during this step.__
   ```bash
   bash setup-ML.sh
   ```
3. Complete the installation of the conda shell with
   ```bash
   bash
   ```
4. To execute any of the python scripts involving Scapy, you will need to use sudo and point to the python binary associated with the ML virtual environment created by Miniforge with:
   ```bash
   sudo ~/miniforge3/envs/ML/bin/python <script>
   ```
5. If you are able to run demo.py and PacketReader.py with the method above, you should be good to go!
