#!/usr/bin/env sh

# Setup pyROOT
export SCRAM_ARCH=slc7_amd64_gcc48
. /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.18.04/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#. /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.20.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

# Inject to PYTHONPATH
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH=${PYTHONPATH}:${DIR}

alias runallsteps="${DIR}/BsToPhiMuMuFitter/bash/RunAllSteps"
alias createpdfs="${DIR}/BsToPhiMuMuFitter/bash/pdfCollection.sh"
alias runfitsteps="${DIR}/BsToPhiMuMuFitter/bash/seqCollection.sh"
alias createplots="${DIR}/BsToPhiMuMuFitter/bash/plotCollection.sh"
alias TotalClean="${DIR}/BsToPhiMuMuFitter/bash/TotalClean.sh"
alias JunkClean="${DIR}/BsToPhiMuMuFitter/bash/JunkClean.sh"

echo -e ">>>> Help <<<< \nCommand: runallsteps\t --> Usage: Run all steps sequestially to produce fit plots\n" 
