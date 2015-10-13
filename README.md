Comet Web Sensor Data Handler
=============================

A simple script for retreiving and dealing with climate data from the Comet T6540 Climate sensor written in Python 3.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Comet Web Sensor Data Handler](#comet-web-sensor-data-handler)
    - [Dependencies](#dependencies)
    - [Installation](#installation)
    - [Usage](#usage)
    - [License](#license)
    - [Development](#development)

<!-- markdown-toc end -->



Dependencies
------------

This project depends on the python module click and the python package manager pip. On Ubuntu they are installed by running:

```bash
sudo apt-get install python3-click python3-pip
```

On all Linux distributions click can be installed through pip, though it's always recommended to use the distribution package manager since those usually come with the promise of semi-automatic security updates.

```bash
sudo pip3 install click
```



Installation
------------

To install from source first install the dependencies detailed above and then run the following:

```bash
git clone https://github.com/Rovanion/comet-sensor.git
cd comet-sensor
sudo pip3 install .
```



Usage
-----

In order to fetch sensor data from your Comet web sensor run the following:

```bash
comet-sensor fetch http://url.to.web.sensor
```

Since at least the T6540 only keeps 1000 data points you should do this at least 1000/samples\_per\_day times a day. Sample rate can be found in the general settings for your web sensor.

Example: The sample rate is once every minute. We should then fetch at least every 0.7 day or once every 16th hour.

But since the sensor clears its memory on reboot it's always safer to fetch more frequently.

You can then use the dump command to export all the gathered data, by default to a file called all_data.csv in the current working directory:

```bash
comet-sensor dump
```



License
-------

You are herby licensed to use this program and all of it's components under the GNU General Public License version 3. A complete copy of the license is available in the LICENSE.txt file and can also be viewed on the [GNU website](http://www.gnu.org/licenses/gpl-3.0.html).



Development
-----------

Development requires a couple additional dependencies:

```bash
sudo pip3 install git-lint
sudo apt-get install virtualenv pep8 pylint
```

It's recommended to use virtualenv for development which allows for setup and other possibly system damaging procedures without actually running the risk of doing so. To set up the virtual environment for the first time, stand in the source code folder and run:

```bash
virtualenv -p /usr/bin/python3 env
```

Then activate the environment, this is the only thing you need to do on consecutive shells you want to develop in:

```bash
source env/bin/activate
```

You can test that you are in the virtualenv by checking that the following command results in a path which ends in your source code folder.

```bash
which python
```

In order to escape the virtualenv one can either close the terminal or run:

```bash
deactivate
```
To install the development version of comet-sensor on your folder into your newly created virtualenv, make sure that you didn't just deactivate it, run:

```bash
pip3 install --editable .
```

To keep everything nice and clean we should also lint our code before commiting it, still standing in the root of the source code folder:

```bash
ln -s `which pre-commit.git-lint.sh` .git/hooks/pre-commit
```
