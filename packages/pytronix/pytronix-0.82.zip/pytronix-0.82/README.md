# Pytronix - One button trace extraction#

This project provides the ability to quickly downloading scope data from a TekTronix digital oscilloscope using the telnet interface.

There are script files that provide the functionality to scrape raw waveform data to an HDF5 file either by using the machine's name or IP address, or to set up a print server which then downloads the data automatically when you press the "print" button on the DSO.

All currently visible channels are downloaded, and all waveform settings are stored in the HDF5 file with the scope data. Direct binary transfer mode is used to make acquisition quick, and files are saved with the timestamp of when the transfer was initiated. If a "print" is initiated from the DSO, the resulting postscript file that the DSO generates is also saved.

Using pytronix provides a convenient "one click" way to save data from a TekTronix DSO for later analysis.

Uses the [telepythic library](https://bitbucket.org/martijnj/telepythic) for handling underlying communications.


### How do I use it? ###
Pytronix provides a number of scripts that do the data acquisition and can be run directly from the command line, as per one of the following examples.

Download all visible traces from the DSO with IP address 192.168.1.10:
```
python pytronix.py 192.168.1.10
```

Start the print server and wait for the DSO to send a print request
```
python pythonix.py
```

Connect to the DSO at 192.168.1.10 and add a printer interface to print to this machine:
```
python configure.py 192.168.1.10
```
