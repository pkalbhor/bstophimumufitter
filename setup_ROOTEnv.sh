#!/usr/bin/env bash

# Setup pyROOT, 
# Compatible with python3 and ROOT 6.23 or higher
export SCRAM_ARCH=slc7_amd64_gcc820
#source /cvmfs/sft.cern.ch/lcg/views/dev3python3/latest/x86_64-centos7-gcc8-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh

# Inject to PYTHONPATH
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH=${PYTHONPATH}:${DIR}

#argcomplete=$(pip3 list | grep argcomplete | wc -l)
#if [ $argcomplete -eq 0 ]
#then
# pip3 install argcomplete --user
#else
# echo "Already installed argcomplete"
#fi

alias python='python3'
alias runallsteps="${DIR}/BsToPhiMuMuFitter/bash/RunAllSteps"
alias createpdfs="${DIR}/BsToPhiMuMuFitter/bash/pdfCollection.sh"
alias runfitsteps="${DIR}/BsToPhiMuMuFitter/bash/seqCollection.sh"
alias createplots="${DIR}/BsToPhiMuMuFitter/bash/plotCollection.sh"
alias TotalClean="${DIR}/BsToPhiMuMuFitter/bash/TotalClean.sh"      #Clean all files created using any command
alias JunkClean="${DIR}/BsToPhiMuMuFitter/bash/JunkClean.sh"        #Clean old libraries

echo -e ">>>> Help <<<< \nRun \n\e[31mpython3 seqCollection.py -h \e[0m\nfor exploring further options \n" 
#var=$(python ${DIR}/BsToPhiMuMuFitter/python/ArgCompletion.py)
#TotList=$(echo "$var" | grep bin1A)
#dirlist=$(echo "$var" | grep seqCollection.py)
#binKey=$(echo "$var" | grep bin1A)
#seqKey=$(echo "$var" | grep fitSig2D)
#plotList=$(echo "$var" | grep effi)

#complete -X '!*.py' -W "$TotList" python
