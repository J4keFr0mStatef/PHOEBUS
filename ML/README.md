# Setting up the ML directory on the Raspberry Pi

1. Navigate to the ML directory.
   ```bash
   cd ~/Admin/SeniorDesign/ML
   ```
2. Execute the setup-ML.sh script. __Do not use sudo during this step.__
   ```bash
   bash setup-ML.sh
   ```
3. To execute any of the python scripts involving Scapy, you will need to use sudo and point to the python binary associated with the ML virtual environment created by Miniforge with:
   ```bash
   sudo /home/Admin/miniforge3/envs/ML/bin/python <script>
   ```
4. If you are able to run demo.py and PacketReader.py with the method above, you should be good to go!
