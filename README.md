# Cash Flow
Automatically constructs a flexible and robust DCF model from any company listed on Capital IQ. Requires a Capital IQ licence and the Capital IQ Excel plugin.

## Required packages
 - Python 3.x
 - xlwings
 - Flask

## Installation and Use
No installation is required beyond Python and the packages indicated above.

There are two options for using this tool:
1. GUI web application
2. Command line

### GUI web application
If you wish to use the tool as a web application, you will need to:
 - Navigate to the root directory
 - Type `flask run` in your terminal
 - Navigate to the server address and follow the instructions

### Command line
If you wish to use the tool without the command line, you will need to:
 - Configure the preferences in `config_data.py`
 - Run `py config.py`
 - The output model should automatically save to the root directory

## Product features
Completed:
 - Excel model template
 - Python backend

In Progress:
 - HTML/CSS template
 - Deploy web application with Flask
 - Host website
