#!/usr/bin/env bash

# Setup pyROOT, 
# Compatible with python3 and ROOT 6.23 or higher
export SCRAM_ARCH=slc7_amd64_gcc820
#source /cvmfs/sft.cern.ch/lcg/views/dev3python3/latest/x86_64-centos7-gcc8-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh

# Inject to PYTHONPATH
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Set PYTHONPATH
[[ "$PYTHONPATH" != *"$DIR"* ]] && export PYTHONPATH=${PYTHONPATH}:${DIR}

# Check for required python modules
argcomplete=$(pip3 list --format=columns | grep filelock | wc -l)
if [ $argcomplete -eq 0 ]
then
    pip3 install filelock --user
else
    echo "Loading..."
fi

alias python='python3'
alias TotalClean="${DIR}/BsToPhiMuMuFitter/bash/TotalClean.sh"      #Clean all files created using any command
alias JunkClean="${DIR}/BsToPhiMuMuFitter/bash/JunkClean.sh"        #Clean old libraries

# Create/Load libraries
python3 ${DIR}/BsToPhiMuMuFitter/cpp/__init__.py
echo -e ">>>>>>>>>>>> Help <<<<<<<<<<<< \nRun \n\e[31mpython3 seqCollection.py -h \e[0m\nfor exploring further options \n" 

