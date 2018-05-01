# AutoCharlie

## Synopsis
AutoCharlie creates and uploads audio archives to the WDRT radio website. It tracks the radio station weekly schedule using the Spinitron API.


## Table of Contents
* [Motivation](#motivation)
* [Environment](#environment)
* [Spinitron API](#spinitron-api)
* [Other Dependencies](#other-dependencies)
* [Installation](#installation)
* [Tests](#tests)
* [Authors](#authors)
* [License](#license)

## Motivation
Audio archives were originally loaded to the WDRT website in a manual fashion. Then radio station volunteer Charlie created a clever script that cobbled together some Mac utilities to automate the process. But that system depended on good internet connectivity to capture an audio stream, and needed regular maitenance. Thus the motivation to create a programmatic solution: AutoCharlie!

## Environment
This project is deployed on Ubuntu 16.04 LTS using python2 (version 2.7)
Installation on various Linux distributions should be straightforward.

## Spinitron API
Spinitron is a tool for creating and sharing radio playlists for non-commercial radio stations.  AutoCharlie consumes Spinitron's API to get the most recent version of WDRT's weekly schedule. The Spinitron API is a read-only, REST/JSON API oriented towards integrating Spinitron data into web sites, mobile apps etc. If you are affiliated with a radio station that already uses Spinitron, you can get a User ID and a Secret for the API by emailing Spinitron.
The code for the python client of the Spinitron API is already included in this repository. A fresh copy can be found at the [SpinPapi bitbucket repo](https://bitbucket.org/spinitron/spinpapi-python-client/src)

## Other Dependencies
* SoX - "SoX is a command-line audio processing tool, particularly suited to making quick, simple edits and to batch processing."
* A file hierarchy containing hour long audio archives (TODO: flesh out description)

## Installation
* `sudo apt-get update && sudo apt-get install sox`
* `git clone https://github.com/Hillmonkey/autocharlie`
* create Hourly and Weekly cron job (see [example-cronjob.txt](example-cronjob.txt))
* update `key.py` to contain the following information:
	* `userid` and `secret` for SpinPapi API
	* Domain Name (`host`) of website that will host audio archives
	* `username`, and SFTP password (`passwd`) for SFTPing audio archives to website
* update `local.py` so that AutoCharlie knows where things are
	* `path`: `~/autocharlie` for example
	* `localStub`: where log files will be sent (make sure that this syncs up with cron job)
	* `remote`: (TODO: choose "remote" or "remoteStub", remoteStub is more consistent)
	* `remoteTesting`: this is a remote folder to send files to when testing a new version of AutoCharlie
	* `archiveSource`: in original use case this folder is NFS mounted
* create a cronjob using ` example-cronjob.txt` as a model

## Tests
No test coverage :(

## Authors

- Larry Madeo - [Github](https://github.com/Hillmonkey) / [Twitter](https://twitter.com/larmalade)

## License
Public Domain. No copywrite protection. 
