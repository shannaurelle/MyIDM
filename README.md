# MyIDM 
A Command Line Interface for downloading files in bulk. Built using Python 3.

## Changelog

v0.1.1 - added test scripts and virtualenv files 

v0.1.2 - refactored code 

## Current Features
1. Runs script using URL as links
2. Can read JSON files for web scraping support

## Dependencies
1. requests : for handling HTTP requests
For more reference, [see the documentation](https://requests.readthedocs.io/en/master/)
2. simplejson : for reading JSON files
For more reference, [see the documentation](https://simplejson.readthedocs.io/en/latest/)

## Usage
#### 1. Installation

1. Install Python 3 first if you don't have it in your computer [Python installation link](https://www.python.org/downloads/)
2. Install the necessary dependencies

Using python pip:

1. requests
> pip install requests
2. simplejson
> pip install simplejson


#### 2. Execution
1. Open the terminal and go to the folder where main.py is located

2. On the terminal type the following
> python main.py -o "destination" -i "inputJSONfile" -f "URL1,URL2,URL3" 

###### Flags
-o -> indicates that the string after it is the folder where you'll store the downloaded file

-i -> indicates that the string after it is the filename of the json file where the URLS are stored

-f -> indicates that the string after it is/are the URL links to the files 

## Versioning
This app is currently at 0.1.0. Versioning is done using semantic versioning.

## Contributions
Want to contribute? Read the open-source guidelines for contributing to this repository.

## Suggestions? Bugs?
Feel free to send an issue to this repository in case of any errors in part of the script.
Note that this script is UNSTABLE for files larger than 4 Mb.

