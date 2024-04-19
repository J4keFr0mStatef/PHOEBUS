#!/bin/bash

#Make sure we are in ML directory
cd ~/SeniorDesign/ML

#Download the miniforge3 installer
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

#Install miniforge3
bash Miniforge3-$(uname)-$(uname -m).sh -b

#Initialize the conda shell
~/miniforge3/condabin/conda init

#Switch to the conda shell
source ~/miniforge3/etc/profile.d/conda.sh

#Update Conda
conda update -n base -c conda-forge conda --yes

#Create the ML environment
conda env create -f environment.yml

#Activate the ML environment
conda activate ML

#Download the model
gdown https://drive.google.com/uc?id=1Ox_maC3SonscRBXQwitmuKexPqJXiW9k