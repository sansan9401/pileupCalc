source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_6_20
cmsenv
cd -
export PYTHON27PATH=$PYTHON27PATH:/usr/lib64/python2.7/site-packages
export PYTHONPATH=${PYTHONPATH#/opt/ohpc/pub/apps/root_6_12_06/lib}
