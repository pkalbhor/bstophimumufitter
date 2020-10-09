# BsToPhiMuMuFitter

This fitter package is designed for ![](http://latex.codecogs.com/svg.latex?B_{s}^{0}\rightarrow{\Phi^{0}\mu\mu}) angular analysis with CMS Run2016/17/18 data.

The core of the fitting procedure, i.e. parts not for this particular analysis, are collected in `v2Fitter` directory. It may be re-used for future works. On the other hand, the customized ones are placed in `BsToPhiMuMuFitter` directory. Please check the `README.md` in each directory for further information

# Setup
The package depends on python3.6 and ROOT6.23 or above.
```bash
git clone -b Dev https://:@gitlab.cern.ch:8443/pkalbhor/bstophimumufitter.git
```
On lxplus, run: (Every time you start Fitter session)

```bash
source setup_ROOTEnv.sh
```

For the first time, you may need to install following pre-requisites with

```bash
pip install --user enum34
```

# Contribute

1. Fork it!
2. Create your new branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request 

# Credits
Original structure of the package is taken from [BuToKstarMuMuV2Fitter](https://github.com/pohsun/BuToKstarMuMuV2Fitter) analysis. 
Thanks to the author [Po-Hsun Chen](https://github.com/pohsun).
