# Klusta: automatic spike sorting up to 64 channels

[![Build Status](https://img.shields.io/travis/kwikteam/klusta.svg)](https://travis-ci.org/kwikteam/klusta)
[![codecov.io](https://img.shields.io/codecov/c/github/kwikteam/klusta.svg)](http://codecov.io/github/kwikteam/klusta?branch=master)
[![Documentation Status](https://readthedocs.org/projects/klusta/badge/?version=latest)](http://klusta.readthedocs.org/en/latest/)
[![PyPI release](https://img.shields.io/pypi/v/klusta.svg)](https://pypi.python.org/pypi/klusta)
[![GitHub release](https://img.shields.io/github/release/kwikteam/klusta.svg)](https://github.com/kwikteam/klusta/releases/latest)

[**klusta**](https://github.com/kwikteam/klusta) is an open source package for automatic spike sorting of multielectrode neurophysiological recordings made with probes containing up to a few dozens of sites.

We are also working actively on more sophisticated algorithms that will scale to hundreds/thousands of channels. This work is being done within the [phy project](https://github.com/kwikteam/phy), which is still experimental at this point.

## Overview

**klusta** implements the following features:

* **Kwik**: An HDF5-based file format that stores the results of a spike sorting session.
* **Spike detection** (also known as SpikeDetekt): an algorithm designed for probes containing tens of channels, based on a flood-fill algorithm in the adjacency graph formed by the recording sites in the probe.
* **Automatic clustering** (also known as Masked KlustaKwik): an automatic clustering algorithm designed for high-dimensional structured datasets.


## GUI

You will need a GUI to visualize the spike sorting results.

We have developed two GUI programs with the same features:

* **KlustaViewa**: older project, but widely used. **This will be automatically installed if you follow the installation instructions below.**
* **phy KwikGUI**: newer project, scales to hundreds/thousands of channels, still experimental. You'll need to install [phy](https://github.com/kwikteam/phy) and [phy-contrib](https://github.com/kwikteam/phy-contrib) if you want to try the development version.

Both GUIs work with the same **Kwik** format.


## Technical details

**klusta** is written in pure Python. The clustering code, written in Python and Cython, currently lives in [another repository](https://github.com/kwikteam/klustakwik2/).


## Quick install guide

**Note**: the installation instructions will be simplified soon.

The following instructions will install both **klusta** and the **KlustaViewa GUI**.

1. Make sure that you have [**miniconda**](http://conda.pydata.org/miniconda.html) installed. You can choose the Python 3.5 64-bit version for your operating system (Linux, Windows, or OS X).
2. **Download the environment file:**
    * [Linux](https://raw.githubusercontent.com/kwikteam/klusta/master/installer/environment-linux.yml)
    * [OS X](https://raw.githubusercontent.com/kwikteam/klusta/master/installer/environment-osx.yml)
    * [Windows](https://raw.githubusercontent.com/kwikteam/klusta/master/installer/environment-win.yml)
3. **Open a terminal** (on Windows, `cmd`, not Powershell) in the directory where you saved the file and type:

    ```bash
    conda install conda=3 --yes
    conda env create -n klusta -f environment-XXX.yml  # replace `XXX` by your system
    source activate klusta  # omit the `source` on Windows
    conda install numpy=1.8 --yes
    ```

4. **Done**! Now, to use klusta and KlustaViewa, you have to first type `source activate klusta` in a terminal (omit the `source` on Windows), and then call `klusta` or `klustaviewa`. See the documentation for more details.

### Updating the software

To get the latest version of the software, open a terminal and type:

```
source activate klusta  # omit the `source` on Windows
pip install klusta klustaviewa kwiklib --upgrade
```

## Links

* [Documentation](http://klusta.readthedocs.org/en/latest/) (work in progress)
* [Paper in Nature Neuroscience (April 2016)](http://www.nature.com/neuro/journal/vaop/ncurrent/full/nn.4268.html)
* [Mailing list](https://groups.google.com/forum/#!forum/klustaviewas)
* [Sample data repository](http://phy.cortexlab.net/data/) (work in progress)


## Credits

**klusta** is developed by [Cyrille Rossant](http://cyrille.rossant.net), [Shabnam Kadir](https://iris.ucl.ac.uk/iris/browse/profile?upi=SKADI56), [Dan Goodman](http://thesamovar.net/), [Max Hunter](https://iris.ucl.ac.uk/iris/browse/profile?upi=MLDHU99), and [Kenneth Harris](https://iris.ucl.ac.uk/iris/browse/profile?upi=KDHAR02), in the [Cortexlab](https://www.ucl.ac.uk/cortexlab), University College London.


