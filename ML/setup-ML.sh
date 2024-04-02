#!/bin/bash

#make sure we are in ML directory
cd /home/Admin/SeniorDesign/ML

#download the miniforge3 installer
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

#install miniforge3
bash Miniforge3-$(uname)-$(uname -m).sh -b

#Add miniforge3 to path:
~/miniforge3/condabin/conda init

#update Conda
conda update -n base -c conda-forge conda --yes

#create the ML environment
conda env create -f environment.yml

#restart the shell
exec bash

#make sure we are STILL in ML directory
cd /home/Admin/SeniorDesign/ML

#activate the ML environment
conda activate ML

#download the model
gdown https://drive.google.com/uc?id=14Od2jOv2_LvyS4ghPlKnrM1ypIYL6sc5