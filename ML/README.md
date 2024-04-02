# Setting up the ML directory on the Raspberry Pi

1. Change your current directory to ~/Admin/SeniorDesign/ML
2. Run
   ```bash
   bash setup-ML.sh
   ```
3. To run any of the python scripts involving Scapy, you will need to use sudo and point to the ML virtual environment created by Conda with:
   ```bash
   sudo /home/Admin/miniforge3/envs/ML/bin/python <script>
   ```
4. If you are able to run demo.py and PacketReader.py with the method above, you should be good to go!
