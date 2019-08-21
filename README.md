# PDI Sci

This module was developed to interface with Artium's Phase Doppler Interferometer (PDI) software. It takes raw CSV files exported from the AIMS gui and processes them to determine:

* Liquid Water Content.
* Drop concentration
* Drop Size Distributions.

This module was created in response to AIMs lack of hands on access to quantities of interest to scientists who were using the device in research settings. It can be implimented from the command line using libcurses module. or imported as a standard package. Fitting of drop size distributions is accomplished using  the [lmfit module](https://lmfit.github.io/lmfit-py/)

### usage
after cloning the package into a local directory, first edit the pdi config file to include the appropriate save directory to your machine. It is recommended to use a virtualenv for installation of appropriate python packages. All necessary packages can be found in the `requirements.txt` file and can be installed using:
```
pip install -r requirements.txt
```
This module is compatible with both python2 and python3 but all recent development has occurred in python3 so use that please.

#### libcurses
The libcurses module provides a more user-friendly and quick way to access the visualizations and features of the PDIsci module. In order to start analysis using the libcurses module run the command:
```
python PDI_driver.py <your data directory> DVT_CH1
```
The second argument of the script indicates the channel to be analyzed. It must be of the form `DVT_CH<X>` where X is 1 or 2. 
 note that executing this from the gnome terminal directly may cause a crash of the terminal after the programn exits. As such, a bash script `PDI.sh` has been included, which can be executed from a GUI to avoid this.
### Further Development 
Currently there has been difficulty getting the fits of drop
