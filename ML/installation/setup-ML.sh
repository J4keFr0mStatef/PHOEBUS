#!/bin/bash

##################################
# Setting up the ML environment  #
##################################

#Download the miniforge3 installer
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

#Install miniforge3
bash Miniforge3-$(uname)-$(uname -m).sh -b -p /etc/phoebus/miniforge3

#Remove the installer
rm Miniforge3-$(uname)-$(uname -m).sh

#Initialize the conda shell
/etc/phoebus/miniforge3/condabin/conda init

#Switch to the conda shell
source /etc/phoebus/miniforge3/etc/profile.d/conda.sh

#Update Conda
conda update -n base -c conda-forge conda --yes

#Create the ML environment
conda env create -f environment.yml

#Activate the ML environment
conda activate ML

#create a ML directory in phoebus
mkdir /etc/phoebus/ML

#Change cwd to ML
cd ~/SeniorDesign/ML

#Download the model
gdown https://drive.google.com/uc?id=1Ox_maC3SonscRBXQwitmuKexPqJXiW9k

#Copy files to phoebus
cp ~/SeniorDesign/ML/MLwriter.py /etc/phoebus/ML/MLwriter.py
cp ~/SeniorDesign/ML/model.pkl /etc/phoebus/ML/model.pkl

##################################
# Scheduling the MLwriter script #
##################################

#Copy the MLwriter.service file to the systemd directory
sudo cp ~/SeniorDesign/ML/installation/MLwriter.service /etc/systemd/system/MLwriter.service

#Reload the systemd daemon
sudo systemctl daemon-reload

#Enable and start the MLwriter service
sudo systemctl enable MLwriter && sudo systemctl start MLwriter