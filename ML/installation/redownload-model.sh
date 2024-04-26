#!/bin/bash

#Change cwd to ML
cd ..

#Switch to the conda shell
source /etc/phoebus/miniforge3/etc/profile.d/conda.sh

#Activate the ML environment
conda activate ML

#Download the model
gdown https://drive.google.com/uc?id=1Ox_maC3SonscRBXQwitmuKexPqJXiW9k

#copy the model to phoebus
cp model.pkl /etc/phoebus/ML/model.pkl